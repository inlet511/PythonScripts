# PythonScripts
一些用python写成的实用工具，包含了学习python过程中涉及到的一些模块

## duplicate_cleaner.py
指定一个目录，找出其中重复的文件并删除
- 包含os.walk的用法
- 根据高效使用md5信息判断文件是否相同的用法

## video_splitter
用于处理从Youtube上下载的长视频，按照章节信息分割视频和字幕
- 包含使用multiProcessing模块的进程池(Pool)处理任务的范例
-  包含调用ffmpeg-python 模块分割视频的范例
- 包含timedelta模块的使用范例

## batch_labeling_tool
- Yolo制作dataset辅助工具
- 批量给图片打 yolo 标签，自动提取图片中心的主体(适用于背景比较干净的浅色的图片)
-  自动清理label
-  自动提取验证组
- 包含opencv模块的使用范例
-  包含argparse的使用范例

## yt-dlp-ui
使用yt-dlp库下载youtube视频的图形界面工具
- 包含pyqt5的使用案例
- 包含调用yt-dlp库的范例

## check_browser_hist
查询chrome浏览记录，找出其中包含某些关键词的记录

- 包含使用asyncio和aiohttp高效进行批量url请求的范例
- 包含sqlite请求数据范例