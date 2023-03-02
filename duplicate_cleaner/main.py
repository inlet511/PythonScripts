import sys
import os
from PyQt5.QtWidgets import QWidget, QApplication,QMainWindow,\
    QPlainTextEdit,QPushButton,QVBoxLayout, QHBoxLayout,QListWidget,\
    QFileDialog,QListWidgetItem,QAbstractItemView
from PyQt5.QtCore import Qt
from duplicate_cleaner import DuplicateCleaner

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 成员变量
        self.root_folder = './'
        self.dup_cleaner = DuplicateCleaner()

        self.setWindowTitle("文件查重")
        self.resize(1000, 800)

        self.set_layout()
        self.set_signal()


    def set_layout(self):
        # 查找到的文件列表容器
        self.list_container = QListWidget()
        self.list_container.setSelectionMode(QAbstractItemView.MultiSelection)

        # 顶部的按钮layout
        btns_layout = QHBoxLayout()
        self.folder_btn = QPushButton("选择文件夹")
        self.analyze_btn = QPushButton("分析")
        self.delete_btn = QPushButton("删除选定")
        btns_layout.addWidget(self.folder_btn)
        btns_layout.addWidget(self.analyze_btn)
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
        self.analyze_btn.clicked.connect(self.analyze_clicked)
        self.delete_btn.clicked.connect(self.delete_selected)

    def open_folder_clicked(self):
        self.list_container.clear()
        self.root_folder = QFileDialog.getExistingDirectory(self,"选择文件夹")
        self.statusBar().showMessage("选定目录:{}".format(self.root_folder))

    def analyze_clicked(self):
        if not os.path.exists(self.root_folder):
            self.statusBar().showMessage("文件夹({})不存在".format(self.root_folder))
            return
        self.statusBar().showMessage("正在分析")
        for filesize, samefiles in self.dup_cleaner.find(self.root_folder):
            # 添加一个不可选择的分割线
            line = QListWidgetItem("{}k-----------------".format(filesize/1024))
            line.setFlags(Qt.NoItemFlags)
            self.list_container.addItem(line)
            for file in samefiles:
                self.list_container.addItem((QListWidgetItem("{}".format(file))))
        self.statusBar().showMessage("分析完成.")


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
