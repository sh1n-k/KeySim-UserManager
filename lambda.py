import json
import boto3
import os
import traceback
from botocore.exceptions import ClientError
from datetime import datetime, timezone

# Initialize DynamoDB client
client = boto3.client('dynamodb')
dynamodb = boto3.resource('dynamodb')

# Get table names from environment variables
USERS_TABLE = os.environ['USERS_TABLE']
AUTH_LOGS_TABLE = os.environ['AUTH_LOGS_TABLE']
ACTIVITY_LOGS_TABLE = os.environ['ACTIVITY_LOGS_TABLE']

def respond(statusCode, body):
    response = {
        'statusCode': statusCode,
        "headers": {
            "Content-Type": "application/json"
        },
        'body': json.dumps(body)
    }
    print(f"Response: {response}")
    return response

def get_current_timestamp():
    return str(int(datetime.now(timezone.utc).timestamp()))

def create_user(user_id):
    print(f"Creating user: {user_id}")
    table = dynamodb.Table(USERS_TABLE)
    try:
        response = table.get_item(Key={'userId': user_id})
        if 'Item' in response:
            return False
        table.put_item(
            Item={
                'userId': user_id,
                'deviceId': '',
                'timestamp': get_current_timestamp()
            },
            ConditionExpression='attribute_not_exists(userId)'
        )
        print(f"User created successfully: {user_id}")
        return True
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            print(f"User already exists: {user_id}")
            return False
        print(f"Error creating user: {user_id}")
        print(f"Error details: {str(e)}")
        raise

def delete_user(user_id):
    print(f"Deleting user: {user_id}")
    table = dynamodb.Table(USERS_TABLE)
    try:
        table.delete_item(Key={'userId': user_id})
        print(f"User deleted successfully: {user_id}")
        return True
    except ClientError as e:
        print(f"Error deleting user: {user_id}")
        print(f"Error details: {str(e)}")
        return False

def reset_user_key(user_id):
    print(f"Resetting key for user: {user_id}")
    table = dynamodb.Table(USERS_TABLE)
    try:
        table.update_item(
            Key={'userId': user_id},
            UpdateExpression='SET deviceId = :val',
            ExpressionAttributeValues={':val': ''}
        )
        print(f"Key reset successfully for user: {user_id}")
        return True
    except ClientError as e:
        print(f"Error resetting key for user: {user_id}")
        print(f"Error details: {str(e)}")
        return False

def get_users():
    print("Fetching all users")
    table = dynamodb.Table(USERS_TABLE)
    try:
        response = table.scan()
        users = response['Items']
        print(f"Retrieved {len(users)} users")
        return users
    except ClientError as e:
        print("Error fetching users")
        print(f"Error details: {str(e)}")
        raise

def authenticate_user(user_id, device_id, timestamp, ip):
    print(f"Authenticating user: {user_id}, Device ID: {device_id}, IP: {ip}")
    table = dynamodb.Table(USERS_TABLE)
    try:
        response = table.get_item(Key={'userId': user_id})
        if 'Item' not in response:
            log_auth(user_id, '403: User not found', device_id, timestamp, False, ip)
            print(f"User not found: {user_id}")
            return 403  # User not found
        
        user = response['Item']
        if not user['deviceId'] or user['deviceId'] == '':
            # Update deviceId if it's empty
            table.update_item(
                Key={'userId': user_id},
                UpdateExpression='SET deviceId = :val',
                ExpressionAttributeValues={':val': device_id}
            )
            log_auth(user_id, '200: Register a device ID', device_id, timestamp, True, ip)
            print(f"Authentication successful for user: {user_id}")
            return 200
        elif user['deviceId'] == device_id:
            # Update deviceId if it matches
            log_auth(user_id, '200: Authentication request', device_id, timestamp, True, ip)
            print(f"Authentication successful for user: {user_id}")
            return 200
        else:
            log_auth(user_id, '401: Authentication failure', device_id, timestamp, False, ip)
            print(f"Device ID mismatch for user: {user_id}")
            return 401  # Device ID mismatch
    except ClientError as e:
        log_auth(user_id, '500: Internal error', device_id, timestamp, False, ip)
        print(f"Error authenticating user: {user_id}")
        print(f"Error details: {str(e)}")
        return 500

def log_auth(user_id, message, device_id, timestamp, success, ip):
    print(f"Logging auth: User: {user_id}, Device: {device_id}, Success: {success}, IP: {ip}")
    table = dynamodb.Table(AUTH_LOGS_TABLE)
    try:
        table.put_item(
            Item={
                'userId': user_id,
                'message': message,
                'timestamp': timestamp,
                'deviceId': device_id,
                'success': success,
                'ip': ip
            }
        )
        print("Auth log recorded successfully")
    except ClientError as e:
        print("Error recording auth log")
        print(f"Error details: {str(e)}")

def log_activity(user_id, message, timestamp, ip):
    print(f"Logging activity: User: {user_id}, Message: {message}, IP: {ip}")
    table = dynamodb.Table(ACTIVITY_LOGS_TABLE)
    try:
        table.put_item(
            Item={
                'userId': user_id,
                'timestamp': timestamp,
                'message': message,
                'ip': ip
            }
        )
        print("Activity log recorded successfully")
    except ClientError as e:
        print("Error recording activity log")
        print(f"Error details: {str(e)}")

def validate_body(body, required_params):
    for param in required_params:
        if param not in body:
            return False, f"Missing required parameter: {param}"
        if not body[param]:
            return False, f"Empty value for required parameter: {param}"
    return True, ""

def lambda_handler(event, context):
    print(f"Received event: {json.dumps(event)}")
    print(f"Context: {context}")
    try:
        method_path = event['routeKey'].split()
        method = method_path[0]
        path = method_path[1]
        body = json.loads(event['body']) if 'body' in event else {}
        ip = event.get('requestContext', {}).get('http', {}).get('sourceIp', 'Unknown')
        body['timestamp'] = get_current_timestamp()

        print(f"Processing request: Path: {path}, Method: {method}")

        # Admin functions
        if path == '/user':
            admin_key = os.environ['ADMIN_KEY']
            if body.get('authKey') != admin_key:
                print("Unauthorized admin access attempt")
                return respond(401, {'message': 'Unauthorized'})

            if method == 'POST':
                valid, error_message = validate_body(body, ['userId'])
                if not valid:
                    return respond(400, {'message': error_message})
                if create_user(body['userId']):
                    return respond(200, {'message': 'User created'})
                else:
                    return respond(400, {'message': 'User already exists'})
            elif method == 'DELETE':
                valid, error_message = validate_body(body, ['userId'])
                if not valid:
                    return respond(400, {'message': error_message})
                if delete_user(body['userId']):
                    return respond(200, {'message': 'User deleted'})
                else:
                    return respond(400, {'message': 'User not found'})
            elif method == 'PUT':
                valid, error_message = validate_body(body, ['userId'])
                if not valid:
                    return respond(400, {'message': error_message})
                if reset_user_key(body['userId']):
                    return respond(200, {'message': 'User key reset'})
                else:
                    return respond(400, {'message': 'User not found'})

        elif path == '/users' and method == 'POST':
            admin_key = os.environ['ADMIN_KEY']
            if body.get('authKey') != admin_key:
                print("Unauthorized admin access attempt")
                return respond(401, {'message': 'Unauthorized'})
            users = get_users()
            return respond(200, {'users': users})

        # Client functions
        elif path == '/auth' and method == 'POST':
            valid, error_message = validate_body(body, ['userId', 'deviceId'])
            if not valid:
                return respond(400, {'message': error_message})
            if len(body["deviceId"]) != 36:
                print(f"Invalid deviceId")
                return respond(401, {'message': 'Invalid Device ID'})

            status = authenticate_user(body['userId'], body['deviceId'], body['timestamp'], ip)
            if status == 200:
                return respond(200, {'message': 'Authentication successful'})
            elif status == 401:
                return respond(401, {'message': 'Device ID mismatch'})
            elif status == 403:
                return respond(403, {'message': 'User not found'})
            else:
                return respond(500, {'message': 'Internal server error'})

        elif path == '/log' and method == 'POST':
            valid, error_message = validate_body(body, ['userId', 'message'])
            if not valid:
                return respond(400, {'message': error_message})
            log_activity(body['userId'], body['message'], body['timestamp'], ip)
            return respond(200, {'message': 'Log recorded'})

        print(f"Unknown path: {path}")
        return respond(404, {'message': 'Not found'})

    except Exception as e:
        print(f"Unexpected error in lambda_handler: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return respond(500, {'message': 'Internal server error'})