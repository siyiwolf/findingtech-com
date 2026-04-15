#!/usr/bin/env python3
"""
Fallback: Upload completed reports to GitHub via REST API (bypass git push)
Target repo: siyiwolf/findingtech-com
"""
import os
import sys
import json
import base64
import zipfile
import tempfile
import requests
from pathlib import Path

# Configuration
REPO = "siyiwolf/findingtech-com"
TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    raise RuntimeError("GITHUB_TOKEN environment variable is required. Set it to your GitHub Personal Access Token.")
API_URL = f"https://api.github.com/repos/{REPO}"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def create_release(tag_name="v2026-04-16-upload", name="Auto Upload 2026-04-16", draft=False, prerelease=False):
    url = f"{API_URL}/releases"
    data = {
        "tag_name": tag_name,
        "target_commitish": "main",
        "name": name,
        "body": "紧急上传：已完成14个方向的洞察报告 (HTML + PDF)",
        "draft": draft,
        "prerelease": prerelease
    }
    resp = requests.post(url, json=data, headers=HEADERS)
    resp.raise_for_status()
    release = resp.json()
    print(f"Created release: {release['html_url']} (id={release['id']})")
    return release

def upload_asset(release, filepath, name=None):
    url = release["upload_url"].split("{")[0] + f"?name={name or os.path.basename(filepath)}"
    with open(filepath, "rb") as f:
        resp = requests.post(url, headers={**HEADERS, "Content-Type": "application/octet-stream"}, data=f)
    resp.raise_for_status()
    asset = resp.json()
    print(f"Uploaded asset: {asset['name']} ({asset['size']} bytes) - {asset['browser_download_url']}")
    return asset

def zip_reports(reports_dir="reports", include_dirs=None):
    if include_dirs is None:
        include_dirs = [d for d in os.listdir(reports_dir) if os.path.isdir(os.path.join(reports_dir, d)) and d.startswith(("0", "1", "2", "3", "4", "5", "6", "7", "8", "9"))]
    zip_path = tempfile.mktemp(suffix=".zip", prefix="reports_")
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for d in include_dirs:
            dirpath = os.path.join(reports_dir, d)
            for root, _, files in os.walk(dirpath):
                for f in files:
                    fp = os.path.join(root, f)
                    arcname = os.path.relpath(fp, start=os.path.dirname(reports_dir))
                    zf.write(fp, arcname)
    print(f"Created zip: {zip_path} ({os.path.getsize(zip_path)} bytes)")
    return zip_path

def main():
    print("Starting fallback upload to GitHub...")
    # Step 1: zip all reports
    zip_path = zip_reports()
    # Step 2: create release
    release = create_release()
    # Step 3: upload zip
    upload_asset(release, zip_path, name=f"reports_{Path(zip_path).stat().st_size // 1024}KB.zip")
    # Optionally upload individual PDFs or HTML (skip for now)
    print("Upload complete. Release URL:", release["html_url"])
    return 0

if __name__ == "__main__":
    sys.exit(main())
