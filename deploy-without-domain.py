import boto3
import json
import time
import os

s3 = boto3.client('s3')
cloudfront = boto3.client('cloudfront')

bucket_name = f'sudoku-cdk-{int(time.time())}'

print(f"Creating S3 bucket: {bucket_name}")
s3.create_bucket(Bucket=bucket_name)

# Block public access
s3.put_public_access_block(
    Bucket=bucket_name,
    PublicAccessBlockConfiguration={
        'BlockPublicAcls': True,
        'IgnorePublicAcls': True,
        'BlockPublicPolicy': True,
        'RestrictPublicBuckets': True
    }
)

# Create CloudFront OAI
oai_response = cloudfront.create_cloud_front_origin_access_identity(
    CloudFrontOriginAccessIdentityConfig={
        'CallerReference': f'sudoku-oai-{int(time.time())}',
        'Comment': 'OAI for Sudoku game'
    }
)
oai_id = oai_response['CloudFrontOriginAccessIdentity']['Id']

# Grant CloudFront access to S3
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {"AWS": f"arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity {oai_id}"},
        "Action": "s3:GetObject",
        "Resource": f"arn:aws:s3:::{bucket_name}/*"
    }]
}
s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))

# Upload files
files = [('sudoku.html', 'text/html'), ('static/style.css', 'text/css')]
for file_path, content_type in files:
    if os.path.exists(file_path):
        key = file_path.replace('static/', '')
        s3.upload_file(file_path, bucket_name, key, ExtraArgs={'ContentType': content_type})
        print(f"Uploaded: {file_path}")

# Create CloudFront distribution
distribution_config = {
    'CallerReference': f'sudoku-dist-{int(time.time())}',
    'Comment': 'Sudoku game distribution',
    'DefaultRootObject': 'sudoku.html',
    'Origins': {
        'Quantity': 1,
        'Items': [{
            'Id': 'S3Origin',
            'DomainName': f'{bucket_name}.s3.amazonaws.com',
            'S3OriginConfig': {
                'OriginAccessIdentity': f'origin-access-identity/cloudfront/{oai_id}'
            }
        }]
    },
    'DefaultCacheBehavior': {
        'TargetOriginId': 'S3Origin',
        'ViewerProtocolPolicy': 'redirect-to-https',
        'TrustedSigners': {'Enabled': False, 'Quantity': 0},
        'ForwardedValues': {'QueryString': False, 'Cookies': {'Forward': 'none'}},
        'MinTTL': 0
    },
    'Enabled': True,
    'PriceClass': 'PriceClass_100'
}

print("Creating CloudFront distribution...")
dist_response = cloudfront.create_distribution(DistributionConfig=distribution_config)
domain_name = dist_response['Distribution']['DomainName']

print(f"\nSudoku Game Deployed Successfully!")
print(f"CloudFront URL: https://{domain_name}")
print(f"S3 Bucket: {bucket_name}")
print(f"Status: Distribution deploying (5-15 minutes)")
print(f"\nBoth URLs will serve the same Sudoku game:")
print(f"1. CloudFront: https://{domain_name}")
print(f"2. Custom Domain: https://samplesrini.com (after DNS setup)")