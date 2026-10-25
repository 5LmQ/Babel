"""独立测试 CategoryTree 的最小入口。

运行方式（在项目根目录）：
    python -m tests.manual_test_category_tree
或直接：
    python tests/manual_test_category_tree.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# 允许从项目根目录直接运行，找到 host 包
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QTextEdit
)

from host.window.category_tree import CategoryTree
from host.manifest.loader import scan_tools


class TestWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Babel")
        self.resize(400, 600)

        self.tree = CategoryTree()
        self.tree.load_plugins(scan_tools(PROJECT_ROOT / "tools"))  # ← 扫描 tools/
        self.tree.plugin_selected.connect(self.on_plugin_selected)

        self.log = QTextEdit()
        self.log.setReadOnly(True)
        self.log.setPlaceholderText("点击左侧叶子节点，这里显示收到的信号")

        container = QWidget()
        layout = QVBoxLayout(container)
        layout.addWidget(QLabel("分类树"))
        layout.addWidget(self.tree)
        layout.addWidget(QLabel("信号日志"))
        layout.addWidget(self.log)
        self.setCentralWidget(container)

    def on_plugin_selected(self, path: str) -> None:
        self.log.append(f"plugin_selected: {path}")


def main() -> int:
    app = QApplication(sys.argv)
    window = TestWindow()
    window.show()
    return app.exec_()


if __name__ == "__main__":
    sys.exit(main())