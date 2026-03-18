#!/bin/bash
# 建立 SpecialInfo Docker image

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

docker build \
  -t nk7260ynpa/tw_stock_specialinfo:latest \
  -f "$SCRIPT_DIR/Dockerfile" \
  "$PROJECT_DIR"
