#!/usr/bin/env python3
import sys
from pathlib import Path

def html_to_pdf(html_path: Path, pdf_path: Path):
    from weasyprint import HTML
    HTML(str(html_path)).write_pdf(str(pdf_path))
    print(f"✅ {pdf_path}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: generate_pdf.py <report_dir>...")
        sys.exit(1)
    for dir_str in sys.argv[1:]:
        dir_path = Path(dir_str)
        html_file = list(dir_path.glob('insight-*.html'))[0]
        pdf_file = html_file.with_suffix('.pdf')
        html_to_pdf(html_file, pdf_file)
