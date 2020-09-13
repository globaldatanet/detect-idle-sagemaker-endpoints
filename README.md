# detect-idle-sagemaker-endpoints
Automatically detecting idle Amazon SageMaker endpoints

1. Create an SNS topic and subscribe your email or phone number to it.
2. Create a Lambda function with the following script.

Your Lambda function should have the following policies attached to its IAM execution role: 
- CloudWatchReadOnlyAccess
- AmazonSNSFullAccess
- AmazonSageMakerReadOnly
