# Serverless ML model monitor

This project contains source code and supporting files for a serverless application for providing real-time inferencing for the HuggingFace Question & Answer Natural Language Processing(NLP) model using [PyTorch](https://pytorch.org/). It also contains a solution to monitor the model performance. The monitoring solution logs the inference request input and the prediction/result from the inference to an S3 bucket using lambda extension. The extension is built as a layer using a makefile and the layer artifacts are copied to the container image along with the inference lambda function. The project includes the following files and folders:

- app/app.py - Code for the application's Lambda function including the code for ML inferencing.
- app/Dockerfile - The Dockerfile to build the container image that packages the inference function, the nodel downloaded from hugging face and the lambda extension built as a layer. The layer cannot be directly attached to the lambda function - so we will be building the layer and copying the layer contents to the container image.
- extensions - The model-monitor-extension files. This lambda extension is used to log the input to the inference function along with the prediction to an S3 bucket.
- app/model - The model downloaded from HuggingFace
- app/requirements.txt - The pip requirements to be installed during the container build.
- events - Invocation events that you can use to invoke the function.
- template.yaml - A template that defines the application's AWS resources.

The application uses several AWS resources, including Lambda functions and an API Gateway API. These resources are defined in the `template.yaml` file in this project. You can update the template to add AWS resources through the same deployment process that updates your application code.

## Deploy the sample application

The Serverless Application Model Command Line Interface (SAM CLI) is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. It uses Docker to run your functions in an Amazon Linux environment that matches Lambda. It can also emulate your application's build environment and API.

To use the SAM CLI, you need the following tools.

- SAM CLI - [Install the SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
- Docker - [Install Docker community edition](https://hub.docker.com/search/?type=edition&offering=community)

You may need the following for local testing.

- [Python 3 installed](https://www.python.org/downloads/)

To build your application for the first time, run the following in your shell. This will build the extension as well:

```bash
sam build
```

Next, build a docker image of the model-monitor-extension layer that's built in the .aws-sam directory.

```bash
docker build -t serverless-ml-model-monitor:latest .
```

Tag your container for deployment to ECR.

```bash
docker tag serverless-ml-model-monitor:latest \
<aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/serverless-ml-model-monitor:latest
```

Login to an ECR repo of your choice to push the extension.

```bash
aws ecr get-login-password --region us-east-1 \
| docker login --username AWS \
--password-stdin <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com
```

Create a repository at ECR.

```bash
aws ecr create-repository \
--repository-name serverless-ml-model-monitor \
--image-scanning-configuration scanOnPush=true \
--region us-east-1
```

Push the container image to ECR.

```bash
docker push <aws-account-id>.dkr.ecr.us-east-1.amazonaws.com/serverless-ml-model-monitor:latest
```

Next, edit line #1 in app/Dockerfile to point to the ECR repo image
Then, uncomment lines #6 and #7 in app/Dockerfile

```bash
WORKDIR /opt
COPY --from=layer /opt/ .
```

The, build the application again

```bash
sam build
```

Finally, deploy the lambda function, API GW and the extension:

```bash
sam deploy --guided
```

This command will package and deploy your application to AWS, with a series of prompts:

- **Stack Name**: The name of the stack to deploy to CloudFormation. This should be unique to your account and region, and a good starting point would be something matching your project name.
- **AWS Region**: The AWS region you want to deploy your app to.
- **Confirm changes before deploy**: If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.
- **Allow SAM CLI IAM role creation**: Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions. To deploy an AWS CloudFormation stack which creates or modifies IAM roles, the `CAPABILITY_IAM` value for `capabilities` must be provided. If permission isn't provided through this prompt, to deploy this example you must explicitly pass `--capabilities CAPABILITY_IAM` to the `sam deploy` command.
- **Save arguments to samconfig.toml**: If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

You can find your API Gateway Endpoint URL in the output values displayed after deployment.

## Testing

To test the application use postman or curl to send a request to the API GW endpoint.
Example:

```bash
curl -X POST -H "Content-Type: text/plain" https://<api-id>.execute-api.us-east-1.amazonaws.com/Prod/nlp-qa -d '{"question": "What is my name?", "context": "My name is Clara and I live in Berkeley."}'
```

## Cleanup

To delete the sample application that you created, use the AWS CLI. Assuming you used your project name for the stack name, you can run the following:

```bash
aws cloudformation delete-stack --stack-name <stack-name>
```

## Resources

See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.

Next, you can use AWS Serverless Application Repository to deploy ready to use Apps that go beyond hello world samples and learn how authors developed their applications: [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)
