#!/usr/bin/env python3

import sys
import boto3

secret_value = sys.argv[1]

ssm_client = boto3.client('ssm')
ssm_client.put_parameter(Type='SecureString', Name='BMCWebhookSecret', Value=secret_value, Overwrite=True)
