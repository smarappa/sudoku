import boto3
import json

s3 = boto3.client('s3')
cloudfront = boto3.client('cloudfront')

bucket_name = 'sudoku-final-1756952030'
distribution_id = 'E1LD984NTKN8WY'

# Get OAI ID from distribution
dist_response = cloudfront.get_distribution(Id=distribution_id)
oai_path = dist_response['Distribution']['DistributionConfig']['Origins']['Items'][0]['S3OriginConfig']['OriginAccessIdentity']
oai_id = oai_path.split('/')[-1]

print(f"Distribution ID: {distribution_id}")
print(f"OAI ID: {oai_id}")

# Fix bucket policy with correct OAI principal
bucket_policy = {
    "Version": "2012-10-17",
    "Statement": [{
        "Sid": "AllowCloudFrontAccess",
        "Effect": "Allow",
        "Principal": {
            "AWS": f"arn:aws:iam::cloudfront:user/CloudFront Origin Access Identity {oai_id}"
        },
        "Action": "s3:GetObject",
        "Resource": f"arn:aws:s3:::{bucket_name}/*"
    }]
}

try:
    s3.put_bucket_policy(Bucket=bucket_name, Policy=json.dumps(bucket_policy))
    print("✓ Bucket policy applied successfully")
except Exception as e:
    print(f"✗ Bucket policy error: {e}")

# Check distribution status
status = dist_response['Distribution']['Status']
domain = dist_response['Distribution']['DomainName']

print(f"Distribution Status: {status}")
print(f"Domain: https://{domain}")

if status == 'InProgress':
    print("⏳ Distribution is still deploying (5-15 minutes)")
    print("⏳ Please wait for deployment to complete")
elif status == 'Deployed':
    print("✓ Distribution is deployed and ready")
    
    # Test access
    import requests
    try:
        response = requests.get(f"https://{domain}", timeout=10)
        print(f"✓ Site accessible: {response.status_code}")
    except Exception as e:
        print(f"✗ Access test failed: {e}")

print(f"\n🌐 Access URL: https://{domain}")
print(f"📦 S3 Bucket: {bucket_name}")