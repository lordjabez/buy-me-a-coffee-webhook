import hashlib
import hmac
import json
import logging
import os

import boto3


secret_name = os.environ['BMC_SECRET_NAME']


_debug_logging = os.environ.get('DEBUG_LOGGING') == 'true'
_log_format = '%(asctime)s : %(levelname)s : %(name)s : %(message)s'
_log_level = logging.DEBUG if _debug_logging else logging.INFO
root_logger = logging.getLogger()
for handler in root_logger.handlers or []:
    root_logger.removeHandler(handler)
logging.basicConfig(format=_log_format, level=_log_level)

_log = logging.getLogger(__name__)


ssm_client = boto3.client('ssm')
response = ssm_client.get_parameter(Name=secret_name, WithDecryption=True)
bmc_secret = response['Parameter']['Value'].encode()


def signature_valid(body, signature):
    digest = hmac.new(bmc_secret, msg=body.encode(), digestmod=hashlib.sha256)
    return signature == digest.hexdigest()


def make_response(code, body={}):
    return {'statusCode': code, 'body': json.dumps(body)}


def log_information(event):
    event_type = event['headers']['x-bmc-event']
    response = json.loads(event['body'])['response']
    name = response.get('supporter_name', 'Unknown Name')
    email = response.get('supporter_email', 'Unknown Email')
    number = int(response['number_of_coffees'])
    amount = float(response['total_amount'])
    _log.info(f'{name} <{email}> purchased {number} coffees for ${amount:.02f} via {event_type}')


def lambda_handler(event, context):
    signature = event['headers']['x-bmc-signature']
    if not signature_valid(event['body'], signature):
        _log.warning('Webhook received with invalid signature')
        return make_response(401, {'error': 'Invalid signature'})
    log_information(event)
    return make_response(200)
