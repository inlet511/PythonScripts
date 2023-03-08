import sys
import os
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QApplication, QGridLayout, QLabel, QLineEdit,
                             QMainWindow, QPushButton, QStatusBar, QToolBar,
                             QVBoxLayout, QWidget)


class DownloaderThread(QThread):
    progressChanged = pyqtSignal(float)

    def __init__(self, url, path):
        super().__init__()
        self.url = url
        self.path = path

    def run(self):
        from yt_dlp import YoutubeDL

        ydl_opts = {
            'outtmpl': self.path + '/%(title)s.%(ext)s',
            'progress_hooks': [self.progress_hook],
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([self.url])

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            progress = d['_percent_str']
            self.progressChanged.emit(float(progress[:-1]))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Youtube Downloader')
        self.setWindowIcon(QIcon('icon.png'))

        # Widgets
        self.url_label = QLabel('URL:')
        self.url_edit = QLineEdit()
        self.path_label = QLabel('Save to:')
        self.path_edit = QLineEdit(os.path.expanduser('~/Downloads'))
        self.download_button = QPushButton('Download')

        # Status bar
        self.statusBar().showMessage('Ready')

        # Tool bar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Layout
        layout = QGridLayout()
        layout.addWidget(self.url_label, 0, 0)
        layout.addWidget(self.url_edit, 0, 1)
        layout.addWidget(self.path_label, 1, 0)
        layout.addWidget(self.path_edit, 1, 1)
        layout.addWidget(self.download_button, 2, 0, 1, 2)

        # Widget
        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        # Connect signals
        self.download_button.clicked.connect(self.download)

    def download(self):
        url = self.url_edit.text()
        path = self.path_edit.text()

        self.thread = DownloaderThread(url, path)
        self.thread.progressChanged.connect(self.update_progress)
        self.thread.finished.connect(self.download_finished)
        self.thread.start()

        self.download_button.setEnabled(False)
        self.statusBar().showMessage('Downloading...')

    def update_progress(self, progress):
        self.statusBar().showMessage(f'Downloading... {progress:.1f}%')

    def download_finished(self):
        self.download_button.setEnabled(True)
        self.statusBar().showMessage('Ready')


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
