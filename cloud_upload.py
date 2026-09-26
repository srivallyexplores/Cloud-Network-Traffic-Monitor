from datetime import datetime
import boto3

BUCKET_NAME = "netmonitor-srivalli-2026-9284"

s3 = boto3.client("s3")

filename = "network_metrics.db"
s3_key = f"metrics/{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}_network_metrics.db"

s3.upload_file(filename, BUCKET_NAME, s3_key)

print("Uploaded to S3 successfully!")
print(f"S3 path: {s3_key}")