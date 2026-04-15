#!/usr/bin/env python3
"""
Upload all reports (HTML+PDF) to GitHub repository via REST API.
Pushes to: siyiwolf/findingtech-com, path: docs/reports/<direction>/
Also creates an index.html in docs/ listing all reports.
"""
import os
import base64
import json
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

def get_branch_sha(branch="main"):
    url = f"{API_URL}/git/refs/heads/{branch}"
    r = requests.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()["object"]["sha"]

def create_tree(base_tree_sha, entries):
    """entries: list of dicts {'path': str, 'mode': '100644', 'type': 'blob', 'content': str/bytes}"""
    url = f"{API_URL}/git/trees"
    data = {
        "base_tree": base_tree_sha,
        "tree": []
    }
    for e in entries:
        entry = {"path": e["path"], "mode": e.get("mode", "100644"), "type": e["type"]}
        if e["type"] == "blob":
            if isinstance(e["content"], str):
                content = e["content"].encode("utf-8")
            else:
                content = e["content"]
            entry["content"] = base64.b64encode(content).decode("utf-8")
        data["tree"].append(entry)
    r = requests.post(url, json=data, headers=HEADERS)
    r.raise_for_status()
    return r.json()["sha"]

def create_commit(message, tree_sha, parent_commit_sha):
    url = f"{API_URL}/git/commits"
    data = {
        "message": message,
        "tree": tree_sha,
        "parents": [parent_commit_sha]
    }
    r = requests.post(url, json=data, headers=HEADERS)
    r.raise_for_status()
    return r.json()["sha"]

def update_ref(ref="heads/main", new_commit_sha=""):
    url = f"{API_URL}/git/refs/{ref}"
    data = {"sha": new_commit_sha, "force": True}
    r = requests.patch(url, json=data, headers=HEADERS)
    r.raise_for_status()
    return r.json()

def upload_file(path, content, is_binary=False):
    """Simplified: create a new commit for each file (slow but reliable)."""
    url = f"{API_URL}/contents/{path}"
    if isinstance(content, bytes):
        content_b64 = base64.b64encode(content).decode("utf-8")
    else:
        content_b64 = base64.b64encode(content.encode("utf-8")).decode("utf-8")
    data = {
        "message": f"Update {path}",
        "content": content_b64,
        "branch": "main"
    }
    r = requests.put(url, json=data, headers=HEADERS)
    if r.status_code == 409:  # conflict, get sha and retry
        existing = requests.get(url, headers=HEADERS).json()
        data["sha"] = existing["sha"]
        r = requests.put(url, json=data, headers=HEADERS)
    r.raise_for_status()
    print(f"Uploaded {path}")
    return r.json()

def collect_report_files(reports_dir="reports"):
    entries = []
    for direction in sorted(os.listdir(reports_dir)):
        dir_path = Path(reports_dir) / direction
        if not dir_path.is_dir():
            continue
        for file in dir_path.iterdir():
            if file.suffix in (".html", ".pdf", ".md"):
                rel_path = f"docs/reports/{direction}/{file.name}"
                entries.append((rel_path, file))
    return entries

def main():
    print("Collecting report files...")
    entries = collect_report_files()
    print(f"Found {len(entries)} files to upload.")
    for path, filepath in entries:
        print(f" - {path}")
        with open(filepath, "rb") as f:
            content = f.read()
        upload_file(path, content, is_binary=True)
    # Create index
    index_content = "<!DOCTYPE html><html><head><meta charset='UTF-8'><title>Reports Index</title></head><body><h1>Insights Reports</h1><ul>"
    for path, _ in entries:
        url = f"https://github.com/{REPO}/blob/main/{path}?raw=true"
        index_content += f'<li><a href="{url}">{path}</a></li>'
    index_content += "</ul></body></html>"
    upload_file("docs/index.html", index_content, is_binary=False)
    print("All files uploaded. Index created.")
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
