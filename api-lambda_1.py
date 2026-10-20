import json

def lambda_handler(event, context):
    # API Gateway proxy integration hands us the whole HTTP request as `event`
    name = "World"
    params = event.get("queryStringParameters") or {}
    if params.get("name"):
        name = params["name"]

    response_data = {
        "message": f"Hello, {name}! Your request was successful.",
        "status": "success",
        "method": event.get("httpMethod"),
        "path": event.get("path"),
    }

    # a proxy integration MUST return this shape
    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(response_data),
    }
