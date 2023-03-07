import ffmpeg
import re
from multiprocessing import Pool

def read_chapter_file(filepath):
    '''
    读取划分章节的文件
    :param filepath:
    :return: 时间-标题数组
    '''
    info_arr = []
    with open(filepath,'r', encoding='utf-8') as f:
        lines = f.readlines()
        invalid_chars = '[\\\/:*?"<>|]'
        replace_char = ''
        for line in lines:
            parts = line.strip().split(' ',1)
            # 去掉文件名的非法字符
            parts[1]=re.sub(invalid_chars,replace_char,parts[1])
            info_arr.append(parts)

    print(info_arr)
    return info_arr


def add_endtime(chapter_list, video_path):
    '''
    添加章节的终止时间
    :param chapter_list:
    :param video_path:
    :return:
    '''
    # 获取视频的长度,如果没有相关信息，则需要手动输入
    duration = ''
    try:
        probe = ffmpeg.probe(video_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        duration = video_stream['tags']['DURATION']
    except:
        duration = input('video contains no duration info, please assign a duration manually:(e.g. 25:37:25.28)')
    # 修改章节列表，增加结束时间
    chapter_cout = len(chapter_list)
    for i in range(chapter_cout):
        end_time = ''
        if i == (chapter_cout - 1):
            end_time = duration
        else:
            end_time = chapter_list[i + 1][0]

        chapter_list[i].insert(1, end_time)
    return chapter_list


def _handle_chapter(video_path, chapter):
    out_file = 'E:/YoutubeDownload/PytorchTutorials/{}.webm'.format(chapter[2])
    print("Creating file: {}".format(out_file))
    (
        ffmpeg
        .input(video_path, ss=chapter[0], to=chapter[1])
        .output(out_file, **{'c:v': 'copy', 'c:a': 'copy'})
        .run()
    )




def split_video(video_path,chapter_list):
    # 启用多个进程同时处理
    pool = Pool(processes=40)

    # 因为处理函数有多个参数，所以需要将参数重新组合
    params = [(video_path, chapter) for chapter in chapter_list]
    pool.starmap(_handle_chapter, params)


if __name__ == '__main__':
    video_file = "E:/YoutubeDownload/PyTorch for Deep Learning & Machine Learning – Full Course [V_xro1bcAuA].webm"
    chapter_list = read_chapter_file("E:/YoutubeDownload/chapters.txt")
    chapter_list = add_endtime(chapter_list, video_path=video_file)
    split_video(video_file, chapter_list)
