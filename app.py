import os

import aws_cdk as cdk
import cdk_nag

from bmc_webhook import BuyMeACoffeeWebhook


app = cdk.App()
env = {'account': os.environ['CDK_DEFAULT_ACCOUNT'], 'region': os.environ['CDK_DEFAULT_REGION']}
stack = BuyMeACoffeeWebhook(app, 'BuyMeACoffeeWebhook', env=env)


cdk.Aspects.of(app).add(cdk_nag.AwsSolutionsChecks(verbose=True))
cdk_nag.NagSuppressions.add_stack_suppressions(stack, [
    {'id': 'AwsSolutions-IAM4', 'reason': 'The webhook Lambda function uses a managed policy for its role'},
])


app.synth()
