import boto3
import time

# Create Route53 hosted zone first
route53 = boto3.client('route53')

try:
    response = route53.create_hosted_zone(
        Name='samplesrini.com',
        CallerReference=str(int(time.time())),
        HostedZoneConfig={
            'Comment': 'Hosted zone for Sudoku game',
            'PrivateZone': False
        }
    )
    
    hosted_zone_id = response['HostedZone']['Id']
    name_servers = response['DelegationSet']['NameServers']
    
    print(f"✅ Created hosted zone: {hosted_zone_id}")
    print(f"📋 Name servers to configure with domain registrar:")
    for ns in name_servers:
        print(f"   - {ns}")
    
    print(f"\n🔧 Next steps:")
    print(f"1. Configure these name servers with your domain registrar")
    print(f"2. Wait for DNS propagation (up to 48 hours)")
    print(f"3. Deploy CDK stack: cdk deploy")
    
except Exception as e:
    if 'HostedZoneAlreadyExists' in str(e):
        print("✅ Hosted zone already exists")
        
        # Get existing hosted zone
        zones = route53.list_hosted_zones_by_name(DNSName='samplesrini.com')
        if zones['HostedZones']:
            zone = zones['HostedZones'][0]
            print(f"📋 Existing zone ID: {zone['Id']}")
    else:
        print(f"❌ Error: {e}")

print(f"\n🚀 Ready to deploy CDK stack with custom domain!")