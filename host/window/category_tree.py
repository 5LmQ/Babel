
from __future__ import annotations

from dataclasses import dataclass, field

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtWidgets import QTreeWidget, QTreeWidgetItem


@dataclass
class PluginInfo:
    name: str
    description: str
    category: str
    path: str
    manifest: dict = field(default_factory=dict)


class CategoryTree(QTreeWidget):
    plugin_selected = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setHeaderLabels(["功能", "描述"])
        self.setColumnWidth(0, 180)
        self.setAlternatingRowColors(True)
        self.setSelectionMode(QTreeWidget.SingleSelection)
        self.setRootIsDecorated(True)

        self._category_items: dict[str, QTreeWidgetItem] = {}

        self.itemClicked.connect(self._on_item_clicked)

    # ---------- 对外 API ----------

    def load_plugins(self, plugins: list[PluginInfo]) -> None:
        """清空并用新插件列表重建树。"""
        self.clear()
        self._category_items.clear()

        grouped: dict[str, list[PluginInfo]] = {}
        for p in plugins:
            grouped.setdefault(p.category or "uncategorized", []).append(p)

        for category in sorted(grouped.keys()):
            cat_item = QTreeWidgetItem([category, ""])
            cat_item.setFlags(cat_item.flags() & ~Qt.ItemIsSelectable)
            font = cat_item.font(0)
            font.setBold(True)
            cat_item.setFont(0, font)
            self.addTopLevelItem(cat_item)
            self._category_items[category] = cat_item

            for plugin in sorted(grouped[category], key=lambda x: x.name.lower()):
                child = QTreeWidgetItem([plugin.name, plugin.description])
                child.setData(0, Qt.UserRole, plugin.path)
                child.setData(0, Qt.UserRole + 1, plugin.manifest)
                child.setToolTip(1, plugin.description)
                cat_item.addChild(child)

        self.expandAll()

    def clear_selection(self) -> None:
        self.setCurrentItem(None)

    # ---------- 内部 ----------

    def _on_item_clicked(self, item: QTreeWidgetItem, column: int) -> None:
        path = item.data(0, Qt.UserRole)
        if path:
            self.plugin_selected.emit(path)