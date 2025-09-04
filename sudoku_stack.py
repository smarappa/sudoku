from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_cloudfront as cloudfront,
    aws_cloudfront_origins as origins,
    aws_s3_deployment as s3deploy,
    aws_certificatemanager as acm,
    aws_route53 as route53,
    aws_route53_targets as route53_targets,
    RemovalPolicy,
    CfnOutput
)
from constructs import Construct

class SudokuStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        bucket = s3.Bucket(
            self, "SudokuBucket",
            removal_policy=RemovalPolicy.DESTROY,
            auto_delete_objects=True,
            block_public_access=s3.BlockPublicAccess.BLOCK_ALL
        )

        # Custom domain setup
        domain_name = "samplesrini.com"
        
        # Get existing hosted zone
        hosted_zone = route53.HostedZone.from_lookup(
            self, "HostedZone",
            domain_name=domain_name
        )
        
        # SSL Certificate
        certificate = acm.Certificate(
            self, "SudokuCertificate",
            domain_name=domain_name,
            subject_alternative_names=[f"*.{domain_name}"],
            validation=acm.CertificateValidation.from_dns(hosted_zone)
        )
        
        oai = cloudfront.OriginAccessIdentity(self, "SudokuOAI")
        bucket.grant_read(oai)

        distribution = cloudfront.Distribution(
            self, "SudokuDistribution",
            default_behavior=cloudfront.BehaviorOptions(
                origin=origins.S3Origin(bucket, origin_access_identity=oai),
                viewer_protocol_policy=cloudfront.ViewerProtocolPolicy.REDIRECT_TO_HTTPS,
                allowed_methods=cloudfront.AllowedMethods.ALLOW_GET_HEAD
            ),
            domain_names=[domain_name],
            certificate=certificate,
            default_root_object="sudoku.html",
            price_class=cloudfront.PriceClass.PRICE_CLASS_100
        )
        
        # Route53 A record
        route53.ARecord(
            self, "SudokuAliasRecord",
            zone=hosted_zone,
            target=route53.RecordTarget.from_alias(
                route53_targets.CloudFrontTarget(distribution)
            )
        )

        s3deploy.BucketDeployment(
            self, "SudokuDeployment",
            sources=[s3deploy.Source.asset(".", exclude=["*.py", "*.json", "requirements.txt", "README.md", "cdk.out", "__pycache__"])],
            destination_bucket=bucket,
            distribution=distribution,
            distribution_paths=["/*"]
        )

        CfnOutput(self, "CustomDomainURL", value=f"https://{domain_name}")
        CfnOutput(self, "DistributionURL", value=f"https://{distribution.distribution_domain_name}")
        CfnOutput(self, "BucketName", value=bucket.bucket_name)