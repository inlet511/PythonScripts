import sys
from PyQt5.Qt import *;
from PyQt5.QtCore import *;
from PyQt5.QtWidgets import *;

# 自定义的item 继承自QListWidgetItem
class customQListWidgetItem(QListWidgetItem):
    def __init__(self, name):
        super().__init__()
        # 自定义item中的widget 用来显示自定义的内容
        self.widget = QWidget()
        # 用来显示name
        self.nameLabel = QLabel()
        self.nameLabel.setText(name)
        # 用来显示avator(图像)
        # 设置图像源 和 图像大小
        # 设置布局用来对nameLabel和avatorLabel进行布局
        self.progress_bar =QProgressBar()
        self.hbox = QHBoxLayout()
        self.hbox.addWidget(self.nameLabel)
        self.hbox.addWidget(self.progress_bar)
        # 设置widget的布局
        self.widget.setLayout(self.hbox)
        # 设置自定义的QListWidgetItem的sizeHint，不然无法显示
        self.setSizeHint(self.widget.sizeHint())

    def text(self):
        return self.nameLabel.text()

    def set_progress(self,progress):
        self.progress_bar.setValue(progress)