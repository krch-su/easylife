#!/bin/bash

set -o errexit
set -o nounset

celery -A project worker -l DEBUG