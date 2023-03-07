from datetime import datetime, timedelta
from splitter import read_chapter_file, add_endtime
import re

def str_to_delta(time_str):
    split = re.split(':|\.', time_str)
    print(split)
    hours,minutes,seconds,microseconds = (0,0,0,0)
    hours = int(split[0]),
    minutes = int(split[1]),
    seconds = int(split[2]),
    if len(split) == 4:
        microseconds = int(split[3])

    return timedelta(hours=hours, minutes=minutes, seconds=seconds, microseconds=microseconds)

if __name__ == '__main__':
    vtt_file = "E:/YoutubeDownload/PyTorch for Deep Learning & Machine Learning – Full Course [V_xro1bcAuA].en.vtt"
    video_file = "E:/YoutubeDownload/PyTorch for Deep Learning & Machine Learning – Full Course [V_xro1bcAuA].webm"

    chapter_list = read_chapter_file("E:/YoutubeDownload/chapters.txt")
    chapter_list = add_endtime(chapter_list, video_path=video_file)
    chapter_list = [(str_to_delta(x[0]), str_to_delta(x[1]), x[2]) for x in chapter_list ]
    print(chapter_list)

    pass
    with open(vtt_file) as vtt:
        # 读取头部
        header = []
        for i in range(3):
            header.append(vtt.readline())

        while True:
            line = vtt.readline()
            if not line:
                break
            line = line.strip()
            if line != '':
                if '-->' in line: # 时间轴
                    line = line.split(' ')
                    start_end = [str_to_delta(line[0]), str_to_delta(line[2])]
                    middle_time = (start_end[0]+start_end[1])/2





