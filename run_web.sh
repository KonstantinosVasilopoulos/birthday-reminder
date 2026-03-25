#!/bin/bash
set -euo pipefail

pip install -r web/requirements.txt --quiet
uvicorn web.app:app --reload
