#!/bin/bash



sleep 10

# FIXME: Maybe check environment variables?
gunicorn --bind 0.0.0.0:5001 --access-logfile - --error-logfile - --log-level debug "app:create_app()"
