# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QListWidgetItem, QFileDialog, QListWidget, QWidget
import multiprocessing as mp
import os
from enum import Enum
from downloader_thread import DownloaderThread


import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class InfoLevel(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3

class Ui_MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1280, 720)

        self.progressBar = None
        self.btn_download = None
        self.btn_clear_tasks = None
        self.horizontalLayout = None
        self.cb_override = None
        self.cb_gen_subtitle = None
        self.cb_subtitle = None
        self.spin_threads = None
        self.label = None
        self.horizontalLayout_4 = None
        self.horizontalLayout_3 = None
        self.le_save_folder = None
        self.btn_select_folder = None
        self.horizontalLayout_2 = None
        self.groupBox_3 = None
        self.lw_urls = None
        self.verticalLayout_2 = None
        self.groupBox_2 = None
        self.btn_add_url = None
        self.le_url = None
        self.horizontalLayout_6 = None
        self.groupBox = None


        # 初始化UI
        self.setupUi()

        #设置最大线程数
        self.setup_cores()

        #关联信号
        self.setup_signals()

    def setupUi(self):

        # 主要Widget容器
        widget = QWidget()

        # 主要 vertical Layout 布局
        verticalLayout = QtWidgets.QVBoxLayout()
        self.setCentralWidget(widget)
        widget.setLayout(verticalLayout)


        # 添加任务行
        self.groupBox = QtWidgets.QGroupBox()
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.groupBox)
        self.le_url = QtWidgets.QLineEdit(self.groupBox)
        self.horizontalLayout_6.addWidget(self.le_url)
        self.btn_add_url = QtWidgets.QPushButton(self.groupBox)
        self.horizontalLayout_6.addWidget(self.btn_add_url)
        verticalLayout.addWidget(self.groupBox)

        # 任务列表行
        self.groupBox_2 = QtWidgets.QGroupBox()
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox_2)
        self.lw_urls = QtWidgets.QListWidget(self.groupBox_2)
        self.lw_urls.setEditTriggers(QtWidgets.QAbstractItemView.AllEditTriggers)
        self.verticalLayout_2.addWidget(self.lw_urls)
        verticalLayout.addWidget(self.groupBox_2)

        # 临时测试用
        self.lw_urls.addItem(QListWidgetItem('https://www.youtube.com/watch?v=_E8rBsPi0Os'))
        self.lw_urls.addItem(QListWidgetItem('https://www.youtube.com/watch?v=AM8D4j9KoaU'))
        self.lw_urls.addItem(QListWidgetItem('https://www.youtube.com/watch?v=x6XgjIHBVyY'))
        self.lw_urls.addItem(QListWidgetItem('https://www.youtube.com/watch?v=AlSCx-4d51U'))
        self.lw_urls.addItem(QListWidgetItem('https://www.youtube.com/watch?v=YOlkttT9kpk'))
        self.lw_urls.addItem(QListWidgetItem('https://www.youtube.com/watch?v=ABd5SmatQi4'))
        self.lw_urls.addItem(QListWidgetItem('https://www.youtube.com/watch?v=eb426KbUc7I'))

        # 保存位置行
        self.groupBox_3 = QtWidgets.QGroupBox()
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.btn_select_folder = QtWidgets.QPushButton(self.groupBox_3)
        self.horizontalLayout_2.addWidget(self.btn_select_folder)
        self.le_save_folder = QtWidgets.QLineEdit(self.groupBox_3)
        self.horizontalLayout_2.addWidget(self.le_save_folder)
        verticalLayout.addWidget(self.groupBox_3)

        # 设置行
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        spacerItem = QtWidgets.QSpacerItem(40, 20)
        self.horizontalLayout_4.addItem(spacerItem)
        self.label = QtWidgets.QLabel()
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        self.horizontalLayout_4.addWidget(self.label)
        self.spin_threads = QtWidgets.QSpinBox()
        self.horizontalLayout_4.addWidget(self.spin_threads)
        self.horizontalLayout_4.setStretch(1, 1)
        self.horizontalLayout_4.setStretch(2, 5)
        self.horizontalLayout_3.addLayout(self.horizontalLayout_4)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.cb_subtitle = QtWidgets.QCheckBox()
        self.cb_subtitle.setChecked(True)
        self.horizontalLayout_3.addWidget(self.cb_subtitle)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.cb_gen_subtitle = QtWidgets.QCheckBox()
        self.horizontalLayout_3.addWidget(self.cb_gen_subtitle)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.cb_override = QtWidgets.QCheckBox()
        self.cb_override.setChecked(True)
        self.horizontalLayout_3.addWidget(self.cb_override)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20)
        self.horizontalLayout_3.addItem(spacerItem4)
        verticalLayout.addLayout(self.horizontalLayout_3)

        # 按钮行
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        spacerItem5 = QtWidgets.QSpacerItem(40, 20)
        self.horizontalLayout.addItem(spacerItem5)
        # 情况任务按钮
        self.btn_clear_tasks = QtWidgets.QPushButton()
        self.btn_clear_tasks.setMinimumSize(QtCore.QSize(200, 40))
        self.horizontalLayout.addWidget(self.btn_clear_tasks)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20)
        self.horizontalLayout.addItem(spacerItem6)
        # 下载按钮
        self.btn_download = QtWidgets.QPushButton()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_download.sizePolicy().hasHeightForWidth())
        self.btn_download.setSizePolicy(sizePolicy)
        self.btn_download.setMinimumSize(QtCore.QSize(200, 40))
        self.horizontalLayout.addWidget(self.btn_download)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20)
        self.horizontalLayout.addItem(spacerItem7)
        verticalLayout.addLayout(self.horizontalLayout)

        # 进度条
        self.progressBar = QtWidgets.QProgressBar()
        self.progressBar.setProperty("value", 24)
        verticalLayout.addWidget(self.progressBar)

        self.progressBar.setValue(0)
        self.progressBar.hide()

        self.retranslateUi()


    def retranslateUi(self):
        self.setWindowTitle("Youtube下载器")
        self.groupBox.setTitle("视频地址")
        self.btn_add_url.setText("添加地址")
        self.groupBox_2.setTitle("任务列表")
        self.groupBox_3.setTitle("保存路径")
        self.btn_select_folder.setText("选择")
        self.le_save_folder.setText("D:/")
        self.label.setText("使用线程数量 :")
        self.cb_subtitle.setText("下载字幕")
        self.cb_gen_subtitle.setText("下载生成字幕")
        self.cb_override.setText("覆盖已有文件")
        self.btn_clear_tasks.setText("清空任务")
        self.btn_download.setText("下载")

    def setup_cores(self):
        core_count = mp.cpu_count()
        self.spin_threads.setMaximum(core_count)
        self.spin_threads.setValue(core_count)

    def select_folder_clicked(self):
        new_folder = QFileDialog.getExistingDirectory(None, "选择保存目录")
        if new_folder != "" and os.path.exists(new_folder):
            self.le_save_folder.setText(new_folder)

    def _url_in_list(list_widget: QListWidget, url):
        for i in range(list_widget.count()):
            if list_widget.item(i).text() == url:
                return True
        return False

    def add_url(self):
        url = self.le_url.text()
        if url:
            if self._url_in_list(self.lw_urls, url):
                self.status_message(InfoLevel.WARNING, "  地址已经存在于列表中", 2000)
            else:
                new_item = QListWidgetItem(url)
                self.lw_urls.addItem(new_item)

    def clear_tasks(self):
        self.lw_urls.clear()

    def status_message(self, level: InfoLevel, txt: str, timespan: int):
        if level == InfoLevel.WARNING:
            stylesheet = 'color:#ed8a11'
        elif level == InfoLevel.INFO:
            stylesheet = 'color: #22b14c'
        elif level == InfoLevel.ERROR:
            stylesheet = 'color: #db0000'
        self.statusBar().setStyleSheet(stylesheet)
        self.statusBar().showMessage(txt, timespan)

    def update_progress(self,progress):
        int_val = int(round(progress))
        self.progressBar.setValue(int_val)

    def download_finished(self):
        self.status_message(InfoLevel.INFO, "下载完成", 0)
        self.progressBar.hide()

    def start_download(self):
        self.progressBar.show()
        self.status_message(InfoLevel.INFO, "下载中", 0)

        # 收集所有地址
        url_list = []

        save_folder = self.le_save_folder.text()
        if not os.path.exists(save_folder):
            logger.warning('指定的路径{}不存在'.format(save_folder))
            self.status_message(InfoLevel.ERROR, "指定的保存路径不存在", 2000)
            return

        for i in range(self.lw_urls.count()):
            url_list.append(self.lw_urls.item(i).text())

        logger.info('获取core_count')
        cores = self.spin_threads.value()

        logger.info('创建线程')
        thread = DownloaderThread(url_list, save_folder, cores)

        thread.progressChanged.connect(self.update_progress)
        thread.finished.connect(self.download_finished)
        thread.start()
        logger.info('开启线程')

    def setup_signals(self):
        self.btn_select_folder.clicked.connect(self.select_folder_clicked)
        self.btn_add_url.clicked.connect(self.add_url)
        self.btn_clear_tasks.clicked.connect(self.clear_tasks)
        self.btn_download.clicked.connect(self.start_download)