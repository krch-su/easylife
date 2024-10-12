#!/bin/bash

set -o errexit
set -o nounset

rm -f './celerybeat.pid'
celery -A project beat -l DEBUG
