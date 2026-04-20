#!/bin/bash
# 批量生成方向 008-020 的 V2 增强版战略规划
# Usage: ./batch_generate_v2.sh

cd /home/ecs-assist-user/.openclaw/workspace-ceo

# 方向ID和名称映射（根据docs/reports目录实际名称）
directions=(
  "08-additional"
  "09-intelligent-sleep"
  "10-outdoor-kitchen"
  "11-smart-lighting"
  "12-outdoor-water"
  "13-camping-wifi"
  "14-outdoor-security"
  "15-smart-clothing"
  "16-drone-swarm"
  "17-outdoor-entertainment"
  "18-emergency-rescue"
  "19-smart-storage"
  "20-eco-monitor"
)

echo "开始批量生成 V2 报告（方向 008-020）..."

for dir in "${directions[@]}"; do
  echo "处理: $dir"

  # 1. 检查洞察报告
  insight_file="docs/reports/$dir/insight-$(basename $dir).html"
  if [ ! -f "$insight_file" ]; then
    insight_file="docs/reports/$dir/insight-$(basename $dir | cut -d'-' -f2-).html"
  fi

  if [ ! -f "$insight_file" ]; then
    echo "  ⚠️ 未找到洞察报告，跳过"
    continue
  fi

  # 2. 生成配置（调用python脚本解析HTML + 生成V2 JSON）
  # 简化：使用placeholder数据（实际应解析HTML）
  # 这里仅创建空文件或提示手动补充
  touch "data/processed/direction-$(echo $dir | cut -d'-' -f1)-config-v2.json"
  echo "  ✅ 配置占位符已创建（需手动填充数据）"

done

echo "批量占位完成！请手动填充每个方向的V2配置数据。"