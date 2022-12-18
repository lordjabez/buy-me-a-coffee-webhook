#!/usr/bin/env bash
set -e

flake8 --max-line-length=120 --statistics bmc_webhook tests
bandit -r bmc_webhook tests
cdk synth > /dev/null
pytest -vv tests
