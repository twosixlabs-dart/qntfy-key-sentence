#!/usr/bin/env sh

set -e

# if ANALYTIC_PORT is set, use it; otherwise 45000
port=${ANALYTIC_PORT:-45000}

# if NUM_WORKERS is set, use it; otherwise 3
workers=${NUM_WORKERS:-3}
worker_timeout=${WORKER_TIMEOUT:-120}

gunicorn -t $worker_timeout --preload --workers $workers --bind 0.0.0.0:$port annotator:app
