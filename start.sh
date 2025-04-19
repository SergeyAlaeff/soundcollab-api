#!/bin/bash
mkdir -p uploads
gunicorn api:app --workers 4 --bind 0.0.0.0:5000
