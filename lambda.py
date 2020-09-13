import boto3
from datetime import datetime
from datetime import timedelta

def lambda_handler(event, context):
    
    idle_threshold_hr = 24               # Change this to your threshold in hours
    
    cw = boto3.client('cloudwatch')
    sm = boto3.client('sagemaker')
    sns = boto3.client('sns')
    
    try:
        inservice_endpoints = sm.list_endpoints(
            SortBy='CreationTime',
            SortOrder='Ascending',
            MaxResults=100,
            # NameContains='string',     # for example 'dev-'
            StatusEquals='InService'
        )
        
        idle_endpoints = []
        for ep in inservice_endpoints['Endpoints']:
            
            ep_describe = sm.describe_endpoint(
                    EndpointName=ep['EndpointName']
                )
    
            metric_response = cw.get_metric_statistics(
                Namespace='AWS/SageMaker',
                MetricName='Invocations',
                Dimensions=[
                    {
                        'Name': 'EndpointName',
                        'Value': ep['EndpointName']
                        },
                        {
                         'Name': 'VariantName',
                        'Value': ep_describe['ProductionVariants'][0]['VariantName']                  
                        }
                ],
                StartTime=datetime.utcnow()-timedelta(hours=idle_threshold_hr),
                EndTime=datetime.utcnow(),
                Period=int(idle_threshold_hr*60*60), 
                Statistics=['Sum'],
                Unit='None'
                )
    
            if len(metric_response['Datapoints'])==0:     
                idle_endpoints.append(ep['EndpointName'])
        
        if len(idle_endpoints) > 0:
            response_sns = sns.publish(
                TopicArn='YOUR SNS TOPIC ARN HERE',
                Message="The following endpoints have been idle for over {} hrs. Log on to Amazon SageMaker console to take actions.\n\n{}".format(idle_threshold_hr, '\n'.join(idle_endpoints)),
                Subject='Automated Notification: Idle Endpoints Detected',
                MessageStructure='string'
            )
    
        return {'Status': 'Success'}
    
    except:
        return {'Status': 'Fail'}
