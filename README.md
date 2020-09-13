# detect-idle-sagemaker-endpoints
Automatically detecting idle Amazon SageMaker endpoints

1. Create an SNS topic and subscribe your email or phone number to it.
2. Create a Lambda function with the following script.

Your Lambda function should have the following policies attached to its IAM execution role: 
- CloudWatchReadOnlyAccess
- AmazonSNSFullAccess
- AmazonSageMakerReadOnly

## Investigating endpoints

This script sends an email (or text message, depending on how the SNS topic is configured) with the list of detected idle endpoints. You can then sign in to the Amazon SageMaker console and investigate those endpoints, and delete them if you find them to be unused stray endpoints. To do so, complete the following steps:

1. On the Amazon SageMaker console, under Inference, choose Endpoints.
You can see the list of all endpoints on your account in that Region.

2. Select the endpoint that you want to investigate, and under Monitor, choose View invocation metrics.
3. Under All metrics, select Invocations
You can see the invocation activities on the endpoint. If you notice no invocation event (or activity) for the duration of your interest, it means the endpoint isn’t in use and you can delete it.

4. When you’re confident you want to delete the endpoint, go back to the list of endpoints, select the endpoint you want to delete, and under the Actions menu, choose
