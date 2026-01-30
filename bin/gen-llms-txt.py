#!/usr/bin/env python3
import sys
import json
import os
import shutil

if len(sys.argv) > 1 and sys.argv[1] == "supports":
    sys.exit(0)

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

book = data[1] if isinstance(data, list) else data.get('book', {})

with open("../llms-full.txt", "w") as f:
    content = []
    def process_item(item):
        if 'Chapter' in item:
            chapter = item['Chapter']
            if not chapter['content'].strip().startswith('#'):
                content.append(f"# {chapter['name']}\n\n")
            content.append(chapter['content'] + "\n\n")
            for sub_item in chapter['sub_items']:
                process_item(sub_item)
    for item in book.get('sections', []):
        process_item(item)
    f.write("".join(content))

html_dir = "../html"
if os.path.exists(html_dir):
    for item in os.listdir(html_dir):
        s = os.path.join(html_dir, item)
        d = os.path.join("..", item)
        if os.path.isdir(s):
            if os.path.exists(d):
                shutil.rmtree(d)
            shutil.copytree(s, d)
        else:
            shutil.copy2(s, d)
    shutil.rmtree(html_dir)

# Try to remove ourselves
# os.chdir("..")
# shutil.rmtree("llms-full-txt")
# Actually, mdbook might not like us deleting the directory we are supposed to render into while it's waiting for us to finish.
# So I'll just leave it. It's empty anyway.
