#!/usr/bin/env python3
"""
批量生成方向 16-20 的 PDF 报告
使用 weasyprint 将 HTML 转换为 PDF
"""

import os
from weasyprint import HTML

# 方向列表
directions = [
    (16, "drone-swarm", "insight-drone-swarm.html"),
    (17, "outdoor-entertainment", "insight-outdoor-entertainment.html"),
    (18, "emergency-rescue", "insight-emergency-rescue.html"),
    (19, "smart-storage", "insight-smart-storage.html"),
    (20, "eco-monitor", "insight-eco-monitor.html"),
]

print("🚀 开始生成方向 16-20 的 PDF 报告...\n")

for num, name, html_file in directions:
    html_path = f"reports/{num:02d}-{name}/{html_file}"
    pdf_path = f"reports/{num:02d}-{name}/insight-{name}.pdf"

    if not os.path.exists(html_path):
        print(f"❌ 跳过 {num:02d}-{name}: HTML 文件不存在")
        continue

    try:
        print(f"📄 生成 PDF: {num:02d}-{name} ...")
        HTML(html_path).write_pdf(pdf_path)
        size_mb = os.path.getsize(pdf_path) / 1024 / 1024
        print(f"   ✅ 完成: {pdf_path} ({size_mb:.2f} MB)")
    except Exception as e:
        print(f"   ❌ 错误: {e}")

print("\n✅ PDF 生成完成!")

# 同时同步到 docs/reports/
print("\n🔄 同步到 docs/reports/ ...")
os.system("rsync -av --delete reports/ docs/reports/ 2>/dev/null")
print("   ✅ 同步完成")
