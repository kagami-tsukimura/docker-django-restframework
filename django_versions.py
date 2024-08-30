import re
import subprocess

# Djangoのバージョン一覧を取得
result = subprocess.run(
    ["pip", "index", "versions", "django"], capture_output=True, text=True
)

# 取得したバージョン一覧をフィルタリング
versions = re.findall(r"\s+(\d+\.\d+\.\d+)", result.stdout)

# 4で始まるバージョンをフィルタリング
filtered_versions = [version for version in versions if version.startswith("4")]

# 改行区切りで表示
for version in filtered_versions:
    print(version)
