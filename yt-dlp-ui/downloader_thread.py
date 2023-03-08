from PyQt5.QtCore import Qt, QThread, pyqtSignal
from yt_dlp import YoutubeDL

class DownloaderThread(QThread):
    # 信号
    progressChanged = pyqtSignal(float)

    def __init__(self, urls, save_path, cores):
        super().__init__()
        self.urls = urls
        self.save_path = save_path
        self.cores = cores

        print("Thread 初始化完成")

    def run(self):
        try:
            ydl_opts = {
                'outtmpl': self.save_path + '/%(title)s.%(ext)s',
                'progress_hooks': [self.progress_hook],
                'concurrent-fragments': self.cores
            }

            print("准备下载")
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download(self.urls)
        except Exception as e:
            print("这里出问题了,", e)

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            progress = d['_percent_str']
            self.progressChanged.emit(float(progress[:-1]))
