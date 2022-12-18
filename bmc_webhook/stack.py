import os

from aws_cdk import Arn, CfnOutput, Duration, Stack
from aws_cdk import aws_iam, aws_lambda


_runtime = aws_lambda.Runtime.PYTHON_3_9
_code_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lambda')

_parameter_name = 'BMCWebhookSecret'


class BuyMeACoffeeWebhook(Stack):

    def __init__(self, scope, construct_id, **kwargs):

        super().__init__(scope, construct_id, **kwargs)

        function = aws_lambda.Function(
            self, 'Webhook',
            runtime=_runtime,
            memory_size=128,
            timeout=Duration.seconds(5),
            code=aws_lambda.Code.from_asset(_code_path),
            handler='handler.lambda_handler',
            environment={
                'BMC_SECRET_NAME': 'BMCWebhookSecret',
            }
        )

        url = function.add_function_url(auth_type=aws_lambda.FunctionUrlAuthType.NONE)

        arn_components = {'service': 'ssm', 'resource': 'parameter', 'resourceName': _parameter_name}
        secret_arn = Arn.format(stack=self, components=arn_components)
        policy_statement = aws_iam.PolicyStatement(
            effect=aws_iam.Effect.ALLOW,
            resources=[secret_arn],
            actions=[
                'ssm:DescribeParameters',
                'ssm:GetParameter',
                'ssm:GetParameterHistory',
                'ssm:GetParameters',
            ],
        )
        secret_policy = aws_iam.Policy(self, 'Secret', statements=[policy_statement])
        function.role.attach_inline_policy(secret_policy)

        CfnOutput(self, 'WebhookUrl', value=url.url)
