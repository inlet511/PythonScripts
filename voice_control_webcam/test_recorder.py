# -*- coding:utf-8 -*-
import subprocess

print("开始录音...")
audio_file = 'output.wav'
# 调用ffmpeg录音
# 获取设备列表的命令： ffmpeg -list_devices true -f dshow -i dummy

command = ['ffmpeg',
           '-y',
           '-f', 'dshow',
           '-i', '''audio=麦克风 (2K USB Camera-Audio)''',
           '-t', '1',
           'output.wav']

result = subprocess.run(command,shell=True)

print("录音结束")