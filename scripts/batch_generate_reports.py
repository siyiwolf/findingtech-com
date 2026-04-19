#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量生成战略规划报告
从 data/processed/*.json 加载配置，生成 HTML + PDF
"""

import os
import json
import re
from pathlib import Path

WORKSPACE = Path("/home/ecs-assist-user/.openclaw/workspace-ceo")
TEMPLATE_PATH = WORKSPACE / "reports/templates/insight-template.html"
OUTPUT_DIR = WORKSPACE / "reports"
DOCS_DIR = WORKSPACE / "docs/reports"

def load_template():
    with open(TEMPLATE_PATH, 'r', encoding='utf-8') as f:
        return f.read()

def load_config(config_path):
    with open(config_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def render_template(template, config):
    """Replace template placeholders ({{KEY}} and {{#each ARRAY}}...{{/each}})"""
    content = template

    # Replace simple fields
    for key, value in config.items():
        if isinstance(value, (str, int, float)):
            placeholder = f"{{{{{key}}}}}"
            content = content.replace(placeholder, str(value))

    # Render {{#each ARRAY}} blocks
    def render_each(match):
        array_name = match.group(1)
        block = match.group(2)
        items = config.get(array_name, [])
        lines = []
        for item in items:
            line = block
            if isinstance(item, dict):
                for k, v in item.items():
                    line = line.replace(f"{{{{this.{k}}}}}", str(v))
            lines.append(line)
        return "\n".join(lines)

    content = re.sub(r'\{\{#each\s+(\w+)\}\}(.*?)\{\{/each\}\}', render_each, content, flags=re.DOTALL)
    return content

def generate_html(config, html_content):
    direction_id = config['direction_id']
    direction_name = config['direction_name']
    direction_title = config['direction_title']

    filename = f"insight-{direction_name}.html"
    output_path = OUTPUT_DIR / f"{direction_id:03d}-{direction_name}" / filename

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    return output_path

def generate_pdf(html_path):
    """使用 pandoc + weasyprint 生成 PDF"""
    pdf_path = html_path.with_suffix('.pdf')
    cmd = f"pandoc {html_path} -o {pdf_path} --pdf-engine=weasyprint --metadata=title='Strategic Report'"
    ret = os.system(cmd)
    if ret != 0:
        print(f"PDF generation failed for {html_path}")
        return None
    return pdf_path

def sync_to_docs(html_path, pdf_path):
    """同步到 docs/reports/ 供 GitHub Pages 使用"""
    direction_name = html_path.parent.name
    docs_dir = DOCS_DIR / direction_name
    docs_dir.mkdir(parents=True, exist_ok=True)

    import shutil
    shutil.copy2(html_path, docs_dir / html_path.name)
    shutil.copy2(pdf_path, docs_dir / pdf_path.name)

    return docs_dir

def main():
    template = load_template()

    # 查找所有 config json
    config_dir = WORKSPACE / "data/processed"
    configs = list(config_dir.glob("direction-*-config.json"))

    print(f"发现 {len(configs)} 个配置，开始生成...")

    for config_file in configs:
        config = load_config(config_file)
        dir_id = config['direction_id']
        dir_name = config['direction_name']

        print(f"生成 {dir_id:03d}-{dir_name} ...", end=" ")

        try:
            html_content = render_template(template, config)
            html_path = generate_html(config, html_content)
            pdf_path = generate_pdf(html_path)

            if pdf_path:
                sync_to_docs(html_path, pdf_path)
                print(f"✅ HTML+PDF (HTML: {html_path.stat().st_size/1024:.1f}KB, PDF: {pdf_path.stat().st_size/1024:.1f}KB)")
            else:
                print(f"❌ PDF失败")
        except Exception as e:
            print(f"❌ 错误: {e}")

    print("\n✅ 全部完成！")

if __name__ == "__main__":
    main()
