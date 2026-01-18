#!/bin/bash

sleep 10

# FIXME: Maybe check environment variables?

gunicorn --bind 0.0.0.0:5000 "app:create_app()"
