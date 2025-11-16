"""
Script để convert tất cả queries từ MySQL sang SQLite
"""

import os
import re


def convert_file(filepath):
    """Convert a Python file from MySQL to SQLite syntax"""
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()

    # Replace %s with ?
    content = content.replace("%s", "?")

    # Replace INSERT IGNORE
    content = content.replace("INSERT IGNORE", "INSERT OR IGNORE")

    # Remove backticks
    content = content.replace("`", "")

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"✓ Converted: {filepath}")


# Convert all model files
models_dir = "models"
for filename in os.listdir(models_dir):
    if filename.endswith(".py"):
        filepath = os.path.join(models_dir, filename)
        convert_file(filepath)

print("\n✅ All models converted to SQLite!")
