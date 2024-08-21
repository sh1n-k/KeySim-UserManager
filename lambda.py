import json
import boto3
import os
from botocore.exceptions import ClientError
from datetime import datetime, timezone

# Initialize DynamoDB resource
dynamodb = boto3.resource('dynamodb')

# Get table names from environment variables
USERS_TABLE = os.environ['USERS_TABLE']
AUTH_LOGS_TABLE = os.environ['AUTH_LOGS_TABLE']
ACTIVITY_LOGS_TABLE = os.environ['ACTIVITY_LOGS_TABLE']
ADMIN_KEY = os.environ['ADMIN_KEY']

def respond(statusCode, body):
    return {
        'statusCode': statusCode,
        "headers": {"Content-Type": "application/json"},
        'body': json.dumps(body)
    }

def get_current_timestamp():
    return str(int(datetime.now(timezone.utc).timestamp()))

def dynamodb_operation(table_name, operation, **kwargs):
    table = dynamodb.Table(table_name)
    try:
        return getattr(table, operation)(**kwargs)
    except ClientError as e:
        print(f"Error in {operation} operation on {table_name}: {str(e)}")
        raise

def create_user(user_id):
    try:
        dynamodb_operation(USERS_TABLE, 'put_item',
            Item={'userId': user_id, 'deviceId': '', 'timestamp': get_current_timestamp()},
            ConditionExpression='attribute_not_exists(userId)'
        )
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return False
        raise

def delete_user(user_id):
    try:
        response = dynamodb_operation(USERS_TABLE, 'delete_item', 
            Key={'userId': user_id},
            ReturnValues='ALL_OLD'
        )
        return 'Attributes' in response
    except ClientError:
        return False

def reset_user_key(user_id):
    try:
        response = dynamodb_operation(USERS_TABLE, 'update_item',
            Key={'userId': user_id},
            UpdateExpression='SET deviceId = :val',
            ExpressionAttributeValues={':val': ''},
            ConditionExpression='attribute_exists(userId)',
            ReturnValues='UPDATED_OLD'
        )
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return False
        raise

def get_users():
    return dynamodb_operation(USERS_TABLE, 'scan')['Items']

def authenticate_user(user_id, device_id, timestamp, ip):
    try:
        user = dynamodb_operation(USERS_TABLE, 'get_item', Key={'userId': user_id}).get('Item')
        if not user:
            log_auth(user_id, '403: User not found', device_id, timestamp, False, ip)
            return 403
        if not user['deviceId']:
            dynamodb_operation(USERS_TABLE, 'update_item',
                Key={'userId': user_id},
                UpdateExpression='SET deviceId = :val',
                ExpressionAttributeValues={':val': device_id}
            )
            log_auth(user_id, '200: Register a device ID', device_id, timestamp, True, ip)
            return 200
        if user['deviceId'] == device_id:
            log_auth(user_id, '200: Authentication request', device_id, timestamp, True, ip)
            return 200
        log_auth(user_id, '401: Authentication failure', device_id, timestamp, False, ip)
        return 401
    except ClientError as e:
        print(f"Error in authenticate_user: {str(e)}")
        log_auth(user_id, '500: Internal server error', device_id, timestamp, False, ip)
        return 500

def log_auth(user_id, message, device_id, timestamp, success, ip):
    try:
        dynamodb_operation(AUTH_LOGS_TABLE, 'put_item',
            Item={
                'userId': user_id,
                'message': message,
                'timestamp': timestamp,
                'deviceId': device_id,
                'success': success,
                'ip': ip
            }
        )
    except ClientError as e:
        print(f"Error in log_auth: {str(e)}")

def log_activity(user_id, message, timestamp, ip):
    try:
        dynamodb_operation(ACTIVITY_LOGS_TABLE, 'put_item',
            Item={
                'userId': user_id,
                'timestamp': timestamp,
                'message': message,
                'ip': ip
            }
        )
    except ClientError as e:
        print(f"Error in log_activity: {str(e)}")

def get_auth_logs(user_id):
    try:
        response = dynamodb_operation(AUTH_LOGS_TABLE, 'query',
            KeyConditionExpression='userId = :userId',
            ExpressionAttributeValues={
                ':userId': user_id,
            },
        )
        return response.get('Items', [])
    except ClientError as e:
        print(f"Error in get_auth_logs: {str(e)}")
        raise


def validate_body(body, required_params):
    missing = [param for param in required_params if not body.get(param)]
    return (True, "") if not missing else (False, f"Missing or empty required parameter(s): {', '.join(missing)}")

def lambda_handler(event, context):
    try:
        method, path = event['routeKey'].split()
        body = json.loads(event.get('body', '{}'))
        ip = event.get('requestContext', {}).get('http', {}).get('sourceIp', 'Unknown')
        body['timestamp'] = get_current_timestamp()
        
        if not path.startswith('/auth') and not path.startswith('/log'):
            if body.get('authKey') != ADMIN_KEY:
                return respond(401, {'message': 'Unauthorized'})
            
        if path.startswith('/log/auth/'):
            if body.get('authKey') != ADMIN_KEY:
                return respond(401, {'message': 'Unauthorized'})
            
            path_params = event["pathParameters"]
            if "user_id" not in path_params or not path_params["user_id"]:
                return respond(400, {'message': 'Empty userId'})
            if method == 'POST':
                auth_logs = get_auth_logs(path_params["user_id"])
                return respond(200, {'logs': auth_logs})

        if path == '/user':
            valid, error_message = validate_body(body, ['userId'])
            if not valid:
                return respond(400, {'message': error_message})
            
            if method == 'POST':
                if create_user(body['userId']):
                    return respond(201, {'message': 'User created'})
                else:
                    return respond(409, {'message': 'User already exists'})
            elif method == 'DELETE':
                if delete_user(body['userId']):
                    return respond(200, {'message': 'User deleted'})
                else:
                    return respond(404, {'message': 'User not found'})
            elif method == 'PUT':
                if reset_user_key(body['userId']):
                    return respond(200, {'message': 'User key reset'})
                else:
                    return respond(404, {'message': 'User not found'})

        elif path == '/users' and method == 'POST':
            return respond(200, {'users': get_users()})

        elif path == '/auth' and method == 'POST':
            valid, error_message = validate_body(body, ['userId', 'deviceId'])
            if not valid:
                return respond(400, {'message': error_message})
            if len(body["deviceId"]) != 36:
                return respond(401, {'message': 'Invalid Device ID'})

            status = authenticate_user(body['userId'], body['deviceId'], body['timestamp'], ip)
            messages = {200: 'Authentication successful', 401: 'Device ID mismatch', 403: 'User not found', 500: 'Internal server error'}
            return respond(status, {'message': messages.get(status, 'Unknown error')})

        elif path == '/log' and method == 'POST':
            valid, error_message = validate_body(body, ['userId', 'message'])
            if not valid:
                return respond(400, {'message': error_message})
            log_activity(body['userId'], body['message'], body['timestamp'], ip)
            return respond(200, {'message': 'Log recorded'})

        return respond(404, {'message': 'Not found'})

    except Exception as e:
        print(f"Unexpected error in lambda_handler: {str(e)}")
        return respond(500, {'message': 'Internal server error'})