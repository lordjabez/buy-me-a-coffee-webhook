import aws_cdk as cdk

import bmc_webhook


def test_function_created():
    app = cdk.App()
    stack = bmc_webhook.BuyMeACoffeeWebhook(app, 'Test')
    template = cdk.assertions.Template.from_stack(stack)
    template.has_resource_properties('AWS::Lambda::Function', {
        'Runtime': 'python3.14',
        'MemorySize': 128,
        'Timeout': 5,
    })
    template.has_output('WebhookUrl', cdk.assertions.Match.any_value())
