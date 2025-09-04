import boto3
import os
from pathlib import Path

# Create S3 client
s3 = boto3.client('s3')
cloudfront = boto3.client('cloudfront')

# Create bucket
bucket_name = 'sudoku-game-' + str(hash(os.getcwd()))[-8:]
try:
    s3.create_bucket(Bucket=bucket_name)
    print(f"Created bucket: {bucket_name}")
except Exception as e:
    print(f"Bucket exists or error: {e}")

# Upload files
files = ['sudoku.html', 'static/style.css']
for file in files:
    if os.path.exists(file):
        key = file.replace('static/', '')
        s3.upload_file(file, bucket_name, key, ExtraArgs={'ContentType': 'text/html' if file.endswith('.html') else 'text/css'})
        print(f"Uploaded: {file}")

# Make bucket public for web hosting
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Sid": "PublicReadGetObject",
        "Effect": "Allow",
        "Principal": "*",
        "Action": "s3:GetObject",
        "Resource": f"arn:aws:s3:::{bucket_name}/*"
    }]
}

import json
s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))

# Enable static website hosting
s3.put_bucket_website(
    Bucket=bucket_name,
    WebsiteConfiguration={
        'IndexDocument': {'Suffix': 'sudoku.html'},
        'ErrorDocument': {'Key': 'sudoku.html'}
    }
)

print(f"Website URL: http://{bucket_name}.s3-website-us-east-1.amazonaws.com")