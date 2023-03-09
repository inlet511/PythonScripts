import json
import logging

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from yt_dlp import YoutubeDL
import time

class DownloaderThread(QThread):
    # 信号
    progressChanged = pyqtSignal(float)
    finishedOne = pyqtSignal()

    def __init__(self, urls, save_path, cores):
        super().__init__()
        self.urls = urls
        self.save_path = save_path
        self.cores = cores

    def run(self):
        try:
            ydl_opts = {
                'outtmpl': self.save_path + '/%(title)s.%(ext)s',
                'progress_hooks': [self.progress_hook],
                'concurrent-fragments': self.cores
            }
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download(self.urls)
        except Exception as e:
            logging.WARNING("下载时出现错误", e)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            progress = d['_percent_str']
            self.progressChanged.emit(float(progress[:-1]))
        elif d['status'] == 'finished':
            self.finishedOne.emit()

class RequestInfoThread(QThread):

    receivedInfo = pyqtSignal(dict)

    def __init__(self, url):
        super().__init__()
        self.url = url
    def run(self):
        ydl_opts = {}
        try:
            with YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(self.url, download=False)
                info = ydl.sanitize_info(info)
                if info is None:
                    print("获取信息失败")
                else:
                    size_mb = info.get('filesize_approx')/1048576
                    size_str = '{:.2f} MB'.format(size_mb)
                    info_dict = {'title': info.get("title"),'filesize': size_str}
                    self.receivedInfo.emit(info_dict)
        except Exception as ex:
            print('获取视频信息时发生错误. {}'.format(ex))

