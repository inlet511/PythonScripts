import sys
from PyQt5.Qt import *;
from PyQt5.QtWidgets import *;

# 自定义的item 继承自QListWidgetItem
class CustomItem(QListWidgetItem):
    def __init__(self, name):
        super().__init__()
        # 自定义item中的widget 用来显示自定义的内容
        self.widget = QWidget()

        # 用来显示name
        self.nameLabel = QLabel()
        self.nameLabel.setText(name)
        self.progress_bar =QProgressBar()

        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.nameLabel)
        self.hbox.addWidget(self.progress_bar)
        # 设置widget的布局
        self.widget.setLayout(self.hbox)
        # 设置自定义的QListWidgetItem的sizeHint，不然无法显示
        self.setSizeHint(self.widget.sizeHint())

    def setBackground(self, widget):
        pallet = widget.pallet()
        pallet.setBrush(10, pallet.base())
        self.setBackground(pallet.brush(widget.backgroundRole()))

    def text(self):
        return self.nameLabel.text()

    def set_progress(self,progress):
        self.progress_bar.setValue(progress)