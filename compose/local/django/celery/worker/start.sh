#!/bin/bash

set -o errexit
set -o nounset

celery -A easylife worker -l INFO