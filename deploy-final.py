import boto3
import os
import time

s3 = boto3.client('s3')
bucket_name = f'sudoku-game-{int(time.time())}'

print(f"Creating bucket: {bucket_name}")
s3.create_bucket(Bucket=bucket_name)

# Wait for bucket to be ready
time.sleep(2)

# Upload files
files = [
    ('sudoku.html', 'text/html'),
    ('static/style.css', 'text/css')
]

for file_path, content_type in files:
    if os.path.exists(file_path):
        key = file_path.replace('static/', '')
        s3.upload_file(
            file_path, bucket_name, key,
            ExtraArgs={'ContentType': content_type}
        )
        print(f"Uploaded: {file_path}")

# Enable static website hosting
s3.put_bucket_website(
    Bucket=bucket_name,
    WebsiteConfiguration={
        'IndexDocument': {'Suffix': 'sudoku.html'}
    }
)

print(f"\n🎮 Sudoku Game Deployed!")
print(f"🌐 Website URL: http://{bucket_name}.s3-website-us-east-1.amazonaws.com")
print(f"📦 Bucket: {bucket_name}")
print("\nNote: Files are private. Access via S3 console to make public if needed.")