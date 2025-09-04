import boto3
import json

# Create CloudWatch and RUM clients
cloudwatch = boto3.client('cloudwatch')
rum = boto3.client('rum')

# Create CloudWatch Dashboard
dashboard_body = {
    "widgets": [
        {
            "type": "metric",
            "properties": {
                "metrics": [
                    ["AWS/CloudFront", "Requests", "DistributionId", "E1LD984NTKN8WY"],
                    [".", "BytesDownloaded", ".", "."],
                    [".", "4xxErrorRate", ".", "."],
                    [".", "5xxErrorRate", ".", "."]
                ],
                "period": 300,
                "stat": "Sum",
                "region": "us-east-1",
                "title": "Sudoku App - CloudFront Metrics"
            }
        },
        {
            "type": "metric",
            "properties": {
                "metrics": [
                    ["AWS/S3", "BucketSizeBytes", "BucketName", "sudoku-game-1756950518", "StorageType", "StandardStorage"],
                    [".", "NumberOfObjects", ".", ".", ".", "."]
                ],
                "period": 86400,
                "stat": "Average",
                "region": "us-east-1",
                "title": "Sudoku App - S3 Storage"
            }
        }
    ]
}

try:
    cloudwatch.put_dashboard(
        DashboardName='SudokuGameMonitoring',
        DashboardBody=json.dumps(dashboard_body)
    )
    print("✓ CloudWatch Dashboard created: SudokuGameMonitoring")
except Exception as e:
    print(f"Dashboard error: {e}")

# Create CloudWatch Alarms
try:
    # High error rate alarm
    cloudwatch.put_metric_alarm(
        AlarmName='SudokuApp-HighErrorRate',
        ComparisonOperator='GreaterThanThreshold',
        EvaluationPeriods=2,
        MetricName='4xxErrorRate',
        Namespace='AWS/CloudFront',
        Period=300,
        Statistic='Average',
        Threshold=5.0,
        ActionsEnabled=False,
        AlarmDescription='Sudoku app high 4xx error rate',
        Dimensions=[
            {'Name': 'DistributionId', 'Value': 'E1LD984NTKN8WY'}
        ]
    )
    print("✓ CloudWatch Alarm created: SudokuApp-HighErrorRate")
except Exception as e:
    print(f"Alarm error: {e}")

print("\nMonitoring Setup Complete!")
print("Dashboard: https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#dashboards:name=SudokuGameMonitoring")
print("\nNext Steps:")
print("1. Replace GA_MEASUREMENT_ID with your Google Analytics ID")
print("2. Configure AWS RUM with your account details")
print("3. Deploy updated HTML file")