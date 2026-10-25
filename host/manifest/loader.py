from __future__ import annotations

import json
import sys
from pathlib import Path

from host.window.category_tree import PluginInfo


def scan_tools(tools_root: str | Path) -> list[PluginInfo]:
    """递归找 tools/ 下所有 manifest.json，返回 PluginInfo 列表。

    坏 manifest 跳过并打日志，不拖垮整个扫描。
    """
    root = Path(tools_root)
    if not root.is_dir():
        print(f"[penknife] tools 目录不存在: {root}", file=sys.stderr)
        return []

    plugins: list[PluginInfo] = []
    for manifest_path in sorted(root.rglob("manifest.json")):
        try:
            data = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as e:
            print(f"[penknife] 跳过坏 manifest: {manifest_path}: {e}", file=sys.stderr)
            continue

        plugin_dir = manifest_path.parent
        # 分类取 tools/<category>/<plugin>/ 里的 <category>；
        # 如果插件直接放在 tools/ 下，就用 "uncategorized"
        rel = plugin_dir.relative_to(root)
        category = rel.parts[0] if len(rel.parts) >= 2 else "uncategorized"

        plugins.append(PluginInfo(
            name=data.get("name") or plugin_dir.name,
            description=data.get("description", ""),
            category=data.get("category") or category,
            path=str(plugin_dir),
            manifest=data,
        ))
    return plugins