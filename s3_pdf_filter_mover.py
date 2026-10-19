import boto3
import urllib.parse
import logging

s3 = boto3.client("s3")
logger = logging.getLogger()
logger.setLevel(logging.INFO)

SOURCE_BUCKET = "uploadanyfiles2026"
DESTINATION_BUCKET = "uploadanyfiles2025"


def lambda_handler(event, context):
    for record in event.get("Records", []):
        # Process only object-created events from the source bucket
        if record.get("eventSource") != "aws:s3":
            continue

        bucket = record["s3"]["bucket"]["name"]

        if bucket != SOURCE_BUCKET:
            continue

        key = urllib.parse.unquote_plus(
            record["s3"]["object"]["key"],
            encoding="utf-8"
        )

        try:
            # Read the uploaded object's metadata
            response = s3.head_object(
                Bucket=bucket,
                Key=key
            )

            content_type = response.get("ContentType", "")
            logger.info(
                "File: %s | Content-Type: %s",
                key,
                content_type
            )

            # Move only files identified as PDFs
            if content_type.lower().split(";")[0].strip() == "application/pdf":

                # Copy the object to the destination bucket
                s3.copy_object(
                    Bucket=DESTINATION_BUCKET,
                    Key=key,
                    CopySource={
                        "Bucket": SOURCE_BUCKET,
                        "Key": key
                    }
                )

                # Delete the source only after a successful copy
                s3.delete_object(
                    Bucket=SOURCE_BUCKET,
                    Key=key
                )

                logger.info(
                    "Moved PDF %s to %s",
                    key,
                    DESTINATION_BUCKET
                )
            else:
                logger.info(
                    "Not a PDF; leaving in source bucket: %s",
                    key
                )

        except Exception:
            logger.exception("Failed to process file: %s", key)
            raise

    return {"statusCode": 200, "body": "Processing complete"}
