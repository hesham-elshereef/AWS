import json

def lambda_handler(event, context):
    token = event.get('authorizationToken')
    
    is_authorized = (token == "my-secret-token")
    effect = "Allow" if is_authorized else "Deny"
    
    return {
        "principalId": "user123",
        "policyDocument": {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Action": "execute-api:Invoke",
                    "Effect": effect,
                    "Resource": event.get('methodArn')
                }
            ]
        }
    }
