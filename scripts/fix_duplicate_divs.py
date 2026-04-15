#!/usr/bin/env python3
"""
Fix duplicate div.slogan and malformed HTML in insight reports.
"""
import re
from pathlib import Path

def fix_html(content: str) -> str:
    # Remove duplicate <div class="slogan">make life easy</div> blocks
    content = re.sub(r'(\s*<div class="slogan">make life easy</div>\s*</div>)+', '', content)
    # Remove stray </div> before proper structure
    content = re.sub(r'^\s*</div>\s*', '', content, flags=re.MULTILINE)
    # Ensure single clean slogan (optional, keep if needed)
    # Fix multiple consecutive closing divs
    content = re.sub(r'</div>\s*</div>\s*</div>+', '</div>', content)
    # Remove any empty meta blocks at the end (duplicate final-meta/final-page)
    # Keep only the last final-meta/final-page if multiple exist
    # Usually the structure ends with final-meta or final-page; ensure only one exists
    # This is a heuristic: if more than one final-meta/final-page, keep the last
    final_meta_pattern = r'(<div class="final-meta".*?</div>|<div class="final-page".*?</div>)'
    matches = list(re.finditer(final_meta_pattern, content, re.DOTALL))
    if len(matches) > 1:
        # Remove all but the last
        for m in matches[:-1]:
            content = content.replace(m.group(0), '')
    # Ensure there's exactly one closing </body></html> at end
    content = re.sub(r'</body>\s*</html>\s*(.*)$', r'</body></html>', content, flags=re.DOTALL)
    return content

def main():
    reports_dir = Path('reports')
    fixed = 0
    for dir_path in sorted(reports_dir.iterdir()):
        if not dir_path.is_dir():
            continue
        html_file = dir_path / f'insight-{dir_path.name}.html'
        if not html_file.exists():
            # Try alternative naming
            html_files = list(dir_path.glob('insight-*.html'))
            if html_files:
                html_file = html_files[0]
            else:
                print(f"⚠️  No insight HTML in {dir_path}")
                continue
        raw = html_file.read_text(encoding='utf-8')
        fixed_content = fix_html(raw)
        if fixed_content != raw:
            html_file.write_text(fixed_content, encoding='utf-8')
            print(f"✅ Fixed {html_file}")
            fixed += 1
        else:
            print(f"⏭️  No change {html_file}")
    print(f"\nTotal fixed: {fixed}")

if __name__ == '__main__':
    main()
