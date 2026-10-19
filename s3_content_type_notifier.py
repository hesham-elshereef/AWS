import json
import urllib.parse
import boto3

print("Loading function")

s3 = boto3.client("s3")
sns = boto3.client("sns", region_name="us-east-1")  # تم تحديث الريجون هنا ليطابق us-east-1

# تم تحديث الـ ARN بالكامل بناءً على ما ظهر في لوحة تحكم AWS لديك
SNS_TOPIC_ARN = "arn:aws:sns:us-east-1:232812966651:file-upload-events-topic"


def lambda_handler(event, context):
    # Get the uploaded file details from the S3 event
    bucket = event["Records"][0]["s3"]["bucket"]["name"]

    key = urllib.parse.unquote_plus(
        event["Records"][0]["s3"]["object"]["key"], encoding="utf-8"
    )

    try:
        # Get the uploaded file's metadata
        response = s3.get_object(Bucket=bucket, Key=key)
        content_type = response["ContentType"]

        print("CONTENT TYPE:", content_type)

        # Publish ONLY the content type to SNS
        sns.publish(TopicArn=SNS_TOPIC_ARN, Message=content_type)

        print("SNS notification sent:", content_type)

        return {"statusCode": 200, "body": content_type}

    except Exception as e:
        print(f"Error processing {key} from bucket {bucket}: {e}")
        raise
