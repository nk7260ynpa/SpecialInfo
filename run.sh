#!/bin/bash
# 啟動 SpecialInfo Dashboard 容器

set -euo pipefail

CONTAINER_NAME="tw-stock-specialinfo"
IMAGE_NAME="nk7260ynpa/tw_stock_specialinfo:latest"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# 停止並移除舊容器
docker rm -f "$CONTAINER_NAME" 2>/dev/null || true

docker run -d \
  --name "$CONTAINER_NAME" \
  --restart=always \
  --network db_network \
  -v "$SCRIPT_DIR/logs:/app/logs" \
  "$IMAGE_NAME"

echo "SpecialInfo Dashboard started (internal only, accessible via db_network as tw-stock-specialinfo:5055)"
