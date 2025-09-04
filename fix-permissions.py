import boto3
import json

s3 = boto3.client('s3')
bucket_name = 'sudoku-game-1756950518'

# Remove block public access
s3.delete_public_access_block(Bucket=bucket_name)

# Set bucket policy for public read
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

s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))

# Make individual files public
files = ['sudoku.html', 'style.css']
for file in files:
    try:
        s3.put_object_acl(Bucket=bucket_name, Key=file, ACL='public-read')
        print(f"Made {file} public")
    except Exception as e:
        print(f"Error with {file}: {e}")

print(f"Fixed permissions for: http://{bucket_name}.s3-website-us-east-1.amazonaws.com")