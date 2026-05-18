#!/bin/bash
set -euo pipefail

pip install -r requirements.txt --quiet
pip install -r web/requirements.txt --quiet
uvicorn web.app:app --reload
