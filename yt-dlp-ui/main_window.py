# -*- coding: utf-8 -*-
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QMainWindow, QFileDialog, QWidget, QTableWidget, \
    QTableWidgetItem, QProgressBar, QGridLayout
import multiprocessing as mp
import os
from enum import Enum
from downloader_thread import DownloaderThread, RequestInfoThread
from request_info_buffer import RequestInfoBuffer

import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


class InfoLevel(Enum):
    INFO = 1
    WARNING = 2
    ERROR = 3



class Ui_MainWindow(QMainWindow):

    exit_signal = pyqtSignal()
    def __init__(self):
        super().__init__()

        # 任务列表Group容器
        self.group_task_table = None
        # 任务列表
        self.task_tbl = None

        # 已完成数量
        self.completed_count = 0

        # 下载线程
        self.download_thread = None

        # 待获取信息列表
        self.request_info_buffer = RequestInfoBuffer()
        # 获取信息线程
        self.request_info_thread = None

        # 启动获取信息线程
        self.request_info_thread = RequestInfoThread(self.request_info_buffer)
        self.request_info_thread.receivedInfo.connect(self.cb_fill_title_size)
        self.exit_signal.connect(self.request_info_thread.stop)
        self.request_info_thread.start()



        self.resize(1280, 800)
        self.btn_download = None
        self.btn_clear_tasks = None
        self.cb_override = None
        self.cb_gen_subtitle = None
        self.cb_subtitle = None
        self.spin_threads = None
        self.label = None
        self.le_save_folder = None
        self.btn_select_folder = None
        self.lw_urls = None
        self.verticalLayout_2 = None
        self.btn_add_url = None
        self.le_url = None

        # 初始化UI
        self.setupUi()

        # 设置最大线程数
        self.setup_cores()

        # 关联信号
        self.setup_signals()


    def closeEvent(self,event):
        self.exit_signal.emit()
        event.accept()

    def set_table_widths(self):
        """
        分配表格各列的宽度
        :return:
        """
        col2_width = 200

        # group 内容区的总宽度
        total_width = self.group_task_table.contentsRect().width()

        self.task_tbl.setColumnWidth(1, col2_width)
        self.task_tbl.setStyleSheet('QTableView { border: none; padding: 0px; }')

        # Get the total width of the table
        remain_width = total_width - col2_width

        # column 1 width
        col1_width = remain_width // 3
        self.task_tbl.setColumnWidth(0, col1_width)

        # column 3 width
        col3_width = remain_width // 3
        self.task_tbl.setColumnWidth(2, col3_width)

        # the last column
        self.task_tbl.horizontalHeader().setStretchLastSection(True)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.set_table_widths()

    def setupUi(self):

        # 主要Widget容器
        widget = QWidget()

        # 主要 Layout 布局
        main_layout = QtWidgets.QVBoxLayout()
        self.setCentralWidget(widget)
        widget.setLayout(main_layout)

        # 添加任务行
        groupBox = QtWidgets.QGroupBox()
        groupBox.setTitle("视频地址")
        horizontalLayout_6 = QtWidgets.QHBoxLayout(groupBox)
        self.le_url = QtWidgets.QLineEdit(groupBox)
        self.le_url.setMinimumHeight(50)
        horizontalLayout_6.addWidget(self.le_url)
        self.btn_add_url = QtWidgets.QPushButton(groupBox)
        self.btn_add_url.setMinimumHeight(50)
        horizontalLayout_6.addWidget(self.btn_add_url)
        main_layout.addWidget(groupBox)

        # 任务列表
        self.group_task_table = QtWidgets.QGroupBox()
        self.group_task_table.setContentsMargins(0, 0, 0, 0)
        self.group_task_table.setTitle("任务列表")
        # 任务表格
        self.task_tbl = QTableWidget(self.group_task_table)
        self.task_tbl.setColumnCount(4)
        self.task_tbl.setHorizontalHeaderLabels(["标题", "大小", "地址", "下载进度"])

        # 内部布局，添加表格
        task_layout = QGridLayout()
        task_layout.addWidget(self.task_tbl, 0, 0)
        self.group_task_table.setLayout(task_layout)

        main_layout.addWidget(self.group_task_table)

        # 临时测试用
        self.add_task(url='https://www.youtube.com/shorts/ThNT2hwiRO4')
        self.add_task(url='https://www.youtube.com/shorts/lJEPiyAIrYY')
        self.add_task(url='https://www.youtube.com/shorts/Ukx2YpGY674')

        # 保存位置行
        groupBox_3 = QtWidgets.QGroupBox()
        groupBox_3.setTitle("保存路径")
        horizontalLayout_2 = QtWidgets.QHBoxLayout(groupBox_3)
        self.btn_select_folder = QtWidgets.QPushButton(groupBox_3)
        self.btn_select_folder.setMinimumHeight(50)
        horizontalLayout_2.addWidget(self.btn_select_folder)
        self.le_save_folder = QtWidgets.QLineEdit(groupBox_3)
        self.le_save_folder.setMinimumHeight(50)
        horizontalLayout_2.addWidget(self.le_save_folder)
        main_layout.addWidget(groupBox_3)

        # 设置行
        horizontalLayout_3 = QtWidgets.QHBoxLayout()
        horizontalLayout_4 = QtWidgets.QHBoxLayout()
        spacerItem = QtWidgets.QSpacerItem(40, 20)
        horizontalLayout_4.addItem(spacerItem)
        self.label = QtWidgets.QLabel()
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter)
        horizontalLayout_4.addWidget(self.label)
        self.spin_threads = QtWidgets.QSpinBox()
        self.spin_threads.setMinimumHeight(50)
        horizontalLayout_4.addWidget(self.spin_threads)
        horizontalLayout_4.setStretch(1, 1)
        horizontalLayout_4.setStretch(2, 5)
        horizontalLayout_3.addLayout(horizontalLayout_4)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20)
        horizontalLayout_3.addItem(spacerItem1)
        self.cb_subtitle = QtWidgets.QCheckBox()
        self.cb_subtitle.setChecked(True)
        horizontalLayout_3.addWidget(self.cb_subtitle)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20)
        horizontalLayout_3.addItem(spacerItem2)
        self.cb_gen_subtitle = QtWidgets.QCheckBox()
        horizontalLayout_3.addWidget(self.cb_gen_subtitle)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20)
        horizontalLayout_3.addItem(spacerItem3)
        self.cb_override = QtWidgets.QCheckBox()
        self.cb_override.setChecked(True)
        horizontalLayout_3.addWidget(self.cb_override)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20)
        horizontalLayout_3.addItem(spacerItem4)
        main_layout.addLayout(horizontalLayout_3)

        # 按钮行
        horizontalLayout = QtWidgets.QHBoxLayout()
        spacerItem5 = QtWidgets.QSpacerItem(40, 20)
        horizontalLayout.addItem(spacerItem5)
        # 情况任务按钮
        self.btn_clear_tasks = QtWidgets.QPushButton()
        self.btn_clear_tasks.setMinimumSize(QtCore.QSize(200, 50))
        horizontalLayout.addWidget(self.btn_clear_tasks)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20)
        horizontalLayout.addItem(spacerItem6)
        # 下载按钮
        self.btn_download = QtWidgets.QPushButton()
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btn_download.sizePolicy().hasHeightForWidth())
        self.btn_download.setSizePolicy(sizePolicy)
        self.btn_download.setMinimumSize(QtCore.QSize(200, 50))
        horizontalLayout.addWidget(self.btn_download)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20)
        horizontalLayout.addItem(spacerItem7)
        main_layout.addLayout(horizontalLayout)

        self.retranslateUi()

    def retranslateUi(self):
        self.setWindowTitle("Youtube下载器")
        self.btn_add_url.setText("添加地址")
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

    def _url_in_list(table_widget: QTableWidget, url):
        for i in range(table_widget.rowCount()):
            if table_widget.item(i, 2) == url:
                return True
        return False

    def cb_fill_title_size(self, data: dict, rowNumber: int):
        self.task_tbl.item(rowNumber, 0).setText(data.get('title'))
        self.task_tbl.item(rowNumber, 1).setText(data.get('filesize'))

    def add_task(self, url):
        rowPos = self.task_tbl.rowCount()
        self.task_tbl.insertRow(rowPos)
        self.task_tbl.setItem(rowPos, 0, QTableWidgetItem())
        self.task_tbl.setItem(rowPos, 1, QTableWidgetItem())
        self.task_tbl.setItem(rowPos, 2, QTableWidgetItem(url))
        self.task_tbl.setCellWidget(rowPos, 3, QProgressBar())

        self.request_info_buffer.put({'row': rowPos, 'url': url})

    def add_task_check(self):
        url = self.le_url.text()
        if url:
            if self._url_in_list(self.task_tbl, url):
                self.status_message(InfoLevel.WARNING, "  地址已经存在于列表中", 2000)
            else:
                self.add_task(url)

    def clear_tasks(self):
        self.task_tbl.clear()

    def status_message(self, level: InfoLevel, txt: str, timespan: int):
        if level == InfoLevel.WARNING:
            stylesheet = 'color:#ed8a11'
        elif level == InfoLevel.INFO:
            stylesheet = 'color: #22b14c'
        elif level == InfoLevel.ERROR:
            stylesheet = 'color: #db0000'
        self.statusBar().setStyleSheet(stylesheet)
        self.statusBar().showMessage(txt, timespan)

    def update_progress(self, progress):
        int_val = int(round(progress))
        item = self.lw_urls.item(self.completed_count)
        item.set_progress(int_val)

    def completed_one(self):
        self.completed_count += 1
        print('Finished Downloading {}'.format(self.completed_count))

    def freeze_ui(self):
        self.btn_download.setEnabled(False)
        self.btn_add_url.setEnabled(False)
        self.btn_clear_tasks.setEnabled(False)
        self.btn_select_folder.setEnabled(False)
        self.spin_threads.setEnabled(False)
        self.cb_gen_subtitle.setEnabled(False)
        self.cb_subtitle.setEnabled(False)
        self.cb_override.setEnabled(False)

    def unfreeze_ui(self):
        self.btn_download.setEnabled(True)
        self.btn_add_url.setEnabled(True)
        self.btn_clear_tasks.setEnabled(True)
        self.btn_select_folder.setEnabled(True)
        self.spin_threads.setEnabled(True)
        self.cb_gen_subtitle.setEnabled(True)
        self.cb_subtitle.setEnabled(True)
        self.cb_override.setEnabled(True)

    def cleanup(self):
        """
        全部下载任务完成以后的清理工作
        :return:
        """
        self.completed_count = 0
        self.unfreeze_ui()

    def tasks_finished(self):
        self.status_message(InfoLevel.INFO, "下载完成", 0)
        self.cleanup()

    def start_download(self):
        self.freeze_ui()
        self.status_message(InfoLevel.INFO, "下载中", 0)

        # 收集所有地址
        url_list = []

        save_folder = self.le_save_folder.text()
        if not os.path.exists(save_folder):
            logger.warning('指定的路径{}不存在'.format(save_folder))
            self.status_message(InfoLevel.ERROR, "指定的保存路径不存在", 2000)
            return

        cores = self.spin_threads.value()

        self.download_thread = DownloaderThread(url_list, save_folder, cores)
        self.download_thread.progressChanged.connect(self.update_progress)
        self.download_thread.finishedOne.connect(self.completed_one)
        self.download_thread.finished.connect(self.tasks_finished)

        self.download_thread.start()

    def setup_signals(self):
        self.btn_select_folder.clicked.connect(self.select_folder_clicked)
        self.btn_add_url.clicked.connect(self.add_task_check)
        self.btn_clear_tasks.clicked.connect(self.clear_tasks)
        self.btn_download.clicked.connect(self.start_download)
