@echo off
echo Installing CDK dependencies...
pip install -r requirements.txt

echo Checking AWS credentials...
aws sts get-caller-identity
if %errorlevel% neq 0 (
    echo AWS credentials not configured. Run: aws configure
    exit /b 1
)

echo Bootstrapping CDK...
cdk bootstrap

echo Deploying Sudoku stack...
cdk deploy --require-approval never

echo Deployment complete!
pause