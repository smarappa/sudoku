import boto3
import time

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
    
    print(f"Created hosted zone: {hosted_zone_id}")
    print(f"Name servers to configure:")
    for ns in name_servers:
        print(f"   - {ns}")
    
    print(f"\nNext steps:")
    print(f"1. Configure name servers with domain registrar")
    print(f"2. Deploy CDK stack: cdk deploy")
    
except Exception as e:
    if 'HostedZoneAlreadyExists' in str(e):
        print("Hosted zone already exists")
        zones = route53.list_hosted_zones_by_name(DNSName='samplesrini.com')
        if zones['HostedZones']:
            zone = zones['HostedZones'][0]
            print(f"Zone ID: {zone['Id']}")
    else:
        print(f"Error: {e}")

print(f"\nReady to deploy CDK stack!")