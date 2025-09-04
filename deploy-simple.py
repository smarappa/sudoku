import boto3
import os

s3 = boto3.client('s3')
bucket_name = 'sudoku-game-' + str(hash(os.getcwd()))[-8:]

# Upload files with public-read ACL
files = [
    ('sudoku.html', 'text/html'),
    ('static/style.css', 'text/css')
]

for file_path, content_type in files:
    if os.path.exists(file_path):
        key = file_path.replace('static/', '')
        s3.upload_file(
            file_path, bucket_name, key,
            ExtraArgs={
                'ContentType': content_type,
                'ACL': 'public-read'
            }
        )
        print(f"Uploaded: {file_path}")

# Enable static website hosting
s3.put_bucket_website(
    Bucket=bucket_name,
    WebsiteConfiguration={
        'IndexDocument': {'Suffix': 'sudoku.html'}
    }
)

region = s3.get_bucket_location(Bucket=bucket_name)['LocationConstraint'] or 'us-east-1'
if region == 'us-east-1':
    url = f"http://{bucket_name}.s3-website-us-east-1.amazonaws.com"
else:
    url = f"http://{bucket_name}.s3-website-{region}.amazonaws.com"

print(f"\n🎮 Sudoku Game Deployed!")
print(f"🌐 Website URL: {url}")
print(f"📦 Bucket: {bucket_name}")