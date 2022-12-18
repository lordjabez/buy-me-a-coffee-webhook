# Buy Me A Coffee Webhook

This repository contains an example implementation of a Lambda function that can
handle an event webhook from [Buy Me A Coffee](https://www.buymeacoffee.com).

Currently this function only logs the received values, but can be extended to
perform any number of actions upon receipt.

Note that the function URL endpoint itself is unauthenticated, but an HMAC signature
check is performed to ensure the webhook call is valid.


## Prerequisites

*  [Python 3](https://www.python.org/downloads/)
*  [AWS CDK](https://aws.amazon.com/cdk/)

Install the requisite packages with `pip3 install -r requirements.txt`.


## Testing

Execute `utilities/run-tests.bash`, which runs three items:

*  `flake8` code quality check
*  `bandit` security vulnerability scan
*  `cdk synth` which includes a `cdk_nag` check defined in `app.py`
*  `pytest` unit tests defined in `tests/test_stack.py`


## Deployment

0. Configure AWS CLI credentials for the account where the solution will be deployed.
1. Deploy the Lambda function with `cdk deploy`. Copy the function URL in the output.
2. Create the webhook [here](https://www.buymeacoffee.com/webhook), pasting in URL from step 1.
   Copy the secret value displayed in the console.
3. Run `utilities/create-secret.py SECRET`, replacing `SECRET` with the copied secret from step 2.


## License

This project is licensed under the MIT-0 License. See the [LICENSE](LICENSE) file for details.
