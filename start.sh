#!/bin/bash
gunicorn api:app --workers 4 --bind 0.0.0.0:$PORT
