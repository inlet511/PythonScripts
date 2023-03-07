import sys
import os
from PyQt5.QtWidgets import QWidget, QApplication,QMainWindow,\
    QPushButton,QVBoxLayout, QHBoxLayout,QListWidget,\
    QFileDialog,QListWidgetItem,QAbstractItemView,QFrame
from PyQt5.QtCore import Qt
from duplicate_cleaner import DuplicateCleaner
import time

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 成员变量
        self.root_folder = './'
        self.dup_cleaner = DuplicateCleaner()

        self.setWindowTitle("文件查重")
        self.resize(1000, 1200)

        self.set_layout()
        self.set_signal()


    def create_seperator(self):
        widget = QWidget()
        layout = QHBoxLayout()
        widget.setLayout(layout)
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken);
        layout.addWidget(line)
        return widget

    def set_layout(self):
        # 查找到的文件列表容器
        self.list_container = QListWidget()
        self.list_container.setSelectionMode(QAbstractItemView.MultiSelection)

        # 顶部的按钮layout
        btns_layout = QHBoxLayout()
        self.folder_btn = QPushButton("选择文件夹")
        self.delete_btn = QPushButton("删除选定")
        btns_layout.addWidget(self.folder_btn)
        btns_layout.addWidget(self.delete_btn)

        # 主体layout
        vlayout = QVBoxLayout()
        vlayout.addLayout(btns_layout)
        vlayout.addWidget(self.list_container)

        # QMainWindow的主体需要放入一个QWidget
        widget = QWidget()
        widget.setLayout(vlayout)

        self.setCentralWidget(widget)

    def set_signal(self):
        self.folder_btn.clicked.connect(self.open_folder_clicked)
        self.delete_btn.clicked.connect(self.delete_selected)

    def open_folder_clicked(self):
        new_folder = QFileDialog.getExistingDirectory(self,"选择文件夹")
        if new_folder != "" and os.path.exists(new_folder):
            self.root_folder = new_folder
            self.statusBar().showMessage("选定目录:{}, 开始分析".format(self.root_folder))
            self.analyze()

    def analyze(self):

        # 每次分析前，先清空列表
        self.list_container.clear()

        # 用于计数和计算耗时
        group_count = 0
        time_start = time.time()

        for filesize, samefiles in self.dup_cleaner.find(self.root_folder):
            # 添加一个不可选择的分割线
            line_widget = self.create_seperator()
            line = QListWidgetItem()

            group_count += 1
            line.setFlags(Qt.NoItemFlags)
            self.list_container.addItem(line)
            self.list_container.setItemWidget(line, line_widget)
            for file in samefiles:
                self.list_container.addItem((QListWidgetItem("{}".format(file))))

        # 计算耗时，格式化耗时字符串
        time_spent_seconds = time.time() - time_start
        print(time_spent_seconds)
        if time_spent_seconds < 0.01:
            time_str = "{:.2f}毫秒".format(time_spent_seconds * 1000)
        else:
            time_str = "{:.2f}秒".format(time_spent_seconds)

        # 状态栏显示执行结果
        if group_count == 0:
            self.statusBar().showMessage(" 分析完成。耗时 {time}，没有重复文件。".format(time=time_str))
        else:
            self.statusBar().showMessage(" 分析完成。耗时 {time}，找到 {groupcount} 组相同文件。".format(time=time_str, groupcount=group_count))

    def delete_selected(self):
        for item in self.list_container.selectedItems():
            os.remove(item.text())
            self.list_container.takeItem(self.list_container.indexFromItem(item).row())
            self.statusBar().showMessage("删除了{}".format(item.text()))
        self.statusBar().showMessage("删除完成")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MyWindow()
    w.show()
    sys.exit(app.exec_())
