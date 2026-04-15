#!/usr/bin/env python3
import os
import base64
from pathlib import Path
import requests

REPO = "siyiwolf/findingtech-com"
TOKEN = os.getenv("GITHUB_TOKEN")
if not TOKEN:
    raise RuntimeError("GITHUB_TOKEN environment variable is required. Set it to your GitHub Personal Access Token.")
API_URL = f"https://api.github.com/repos/{REPO}"
HEADERS = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def upload_file(path, content, sha=None):
    """Upload or update a single file on GitHub."""
    url = f"{API_URL}/contents/{path}"
    content_b64 = base64.b64encode(content).decode("utf-8")
    data = {
        "message": f"{'Update' if sha else 'Create'} {path}",
        "content": content_b64,
        "branch": "main"
    }
    if sha:
        data["sha"] = sha
    r = requests.put(url, json=data, headers=HEADERS)
    if r.status_code not in (201, 200):
        print(f"Failed to upload {path}: {r.status_code} {r.text[:200]}")
        r.raise_for_status()
    print(f"{'Updated' if sha else 'Created'} {path}")
    return r.json()

def get_file_sha(path):
    url = f"{API_URL}/contents/{path}"
    r = requests.get(url, headers=HEADERS)
    if r.status_code == 200:
        return r.json()["sha"]
    return None

def ensure_dir_exists(path):
    """Ensure a directory exists on GitHub by creating a .gitkeep if necessary."""
    # GitHub API automatically creates directories; no need to explicitly create
    pass

def main():
    reports_dir = "reports"
    # Collect all HTML and PDF files
    files = []
    for direction in sorted(os.listdir(reports_dir)):
        dir_path = Path(reports_dir) / direction
        if not dir_path.is_dir():
            continue
        for file in dir_path.iterdir():
            if file.suffix in (".html", ".pdf", ".md", ".txt"):
                rel_path = f"docs/reports/{direction}/{file.name}"
                files.append((rel_path, file))

    print(f"Found {len(files)} files to upload.")

    for path, filepath in files:
        with open(filepath, "rb") as f:
            content = f.read()
        # Check if file exists to get its sha
        sha = get_file_sha(path)
        # Upload with appropriate sha if exists
        try:
            upload_file(path, content, sha=sha)
        except requests.exceptions.HTTPError as e:
            print(f"Error uploading {path}: {e}")

    # Create or update index.html
    index_path = "docs/index.html"
    index_content = "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Reports Index</title></head><body><h1>Insights Reports</h1><ul>"
    for path, _ in files:
        raw_url = f"https://github.com/{REPO}/blob/main/{path}?raw=true"
        index_content += f'<li><a href="{raw_url}">{path}</a></li>'
    index_content += "</ul></body></html>"
    sha_idx = get_file_sha(index_path)
    try:
        upload_file(index_path, index_content.encode("utf-8"), sha=sha_idx)
    except requests.exceptions.HTTPError as e:
        print(f"Error uploading index: {e}")

    print("All done.")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
