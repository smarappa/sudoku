import boto3
import json
import time

s3 = boto3.client('s3')
cloudfront = boto3.client('cloudfront')

bucket_name = 'sudoku-final-1756952030'
distribution_id = 'E1LD984NTKN8WY'

# Get distribution details
dist_response = cloudfront.get_distribution(Id=distribution_id)
status = dist_response['Distribution']['Status']
domain = dist_response['Distribution']['DomainName']

print(f"Distribution Status: {status}")
print(f"Domain: https://{domain}")

# Get OAI and fix bucket policy
oai_path = dist_response['Distribution']['DistributionConfig']['Origins']['Items'][0]['S3OriginConfig']['OriginAccessIdentity']
oai_id = oai_path.split('/')[-1]

bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Effect": "Allow",
        "Principal": {"AWS": f"arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity {oai_id}"},
        "Action": "s3:GetObject",
        "Resource": f"arn:aws:s3:::{bucket_name}/*"
    }]
}

try:
    s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))
    print("Bucket policy applied")
except Exception as e:
    print(f"Policy error: {e}")

if status == 'InProgress':
    print("Distribution still deploying - wait 10-15 minutes")
elif status == 'Deployed':
    print("Distribution ready!")
    print(f"Test URL: https://{domain}")

print(f"\nCurrent time: {time.strftime('%H:%M:%S')}")
print("Check again in 5 minutes if still deploying")