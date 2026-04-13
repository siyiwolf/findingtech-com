#!/bin/bash

# Git Push Auto-Retry Script
# 自动重试GitHub推送，应对网络不稳定

set -e

cd /home/ecs-assist-user/.openclaw/workspace-ceo

# 配置（如果未设置）
git config --local http.postBuffer 524288000 2>/dev/null || true
git config --local http.version HTTP/1.1 2>/dev/null || true
git config --local http.lowspeedLimit 0 2>/dev/null || true
git config --local http.lowspeedTime 999 2>/dev/null || true

# 检查是否有未推送的提交
UNPUSHED=$(git log --oneline origin/main..HEAD 2>/dev/null | wc -l)

if [ "$UNPUSHED" -eq 0 ]; then
  echo "$(date '+%Y-%m-%d %H:%M:%S') - ✅ 无待推送提交"
  exit 0
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') - ⏳ 发现 $UNPUSHED 个待推送提交，开始重试..."

# 重试逻辑
MAX_RETRIES=10
DELAY=5

for i in $(seq 1 $MAX_RETRIES); do
  echo "尝试 $i/$MAX_RETRIES..."
  if git push origin main --no-verify 2>&1; then
    echo "$(date '+%Y-%m-%d %H:%M:%S') - ✅ 推送成功！"
    exit 0
  fi
  echo "推送失败，${DELAY}秒后重试..."
  sleep $DELAY
  DELAY=$((DELAY * 2))  # 指数退避
done

echo "$(date '+%Y-%m-%d %H:%M:%S') - ❌ 所有重试失败，请手动推送或应用补丁"
exit 1
