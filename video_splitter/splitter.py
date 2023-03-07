import ffmpeg
import re
from multiprocessing import Pool
from datetime import timedelta
import os


def read_chapter_file(filepath):
    '''
    读取划分章节的文件
    :param filepath:
    :return: 时间-标题数组
    '''
    info_arr = []
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        invalid_chars = '[\\\/:*?"<>|]'
        replace_char = ''
        for line in lines:
            parts = line.strip().split(' ', 1)
            # 去掉文件名的非法字符
            parts[1] = re.sub(invalid_chars, replace_char, parts[1])
            info_arr.append(parts)

    print(info_arr)
    return info_arr


def add_endtime(in_chapter_list, video_path):
    """
    添加章节的终止时间
    :param in_chapter_list:
    :param video_path:
    :return:
    """
    # 获取视频的长度,如果没有相关信息，则需要手动输入
    duration = ''
    try:
        probe = ffmpeg.probe(video_path)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        duration = video_stream['tags']['DURATION']
    except KeyError:
        duration = input('video contains no duration info, please assign a duration manually:(e.g. 25:37:25.28)')
    # 修改章节列表，增加结束时间
    chapter_count = len(in_chapter_list)
    for i in range(chapter_count):
        end_time = ''
        if i == (chapter_count - 1):
            end_time = duration
        else:
            end_time = in_chapter_list[i + 1][0]

        in_chapter_list[i].insert(1, end_time)
    return in_chapter_list


def _handle_chapter(video_path, chapter, in_output_root):
    out_file = '{root}/{name}.webm'.format(root=in_output_root, name=chapter[2])
    print("Creating file: {}".format(out_file))
    (
        ffmpeg
        .input(video_path, ss=chapter[0], to=chapter[1])
        .output(out_file, **{'c:v': 'copy', 'c:a': 'copy'})
        .run()
    )


def split_video(video_path, in_output_root, in_chapter_list):
    # 启用多个进程同时处理
    pool = Pool(processes=40)

    # 因为处理函数有多个参数，所以需要将参数重新组合
    params = [(video_path, chapter, in_output_root) for chapter in in_chapter_list]
    pool.starmap(_handle_chapter, params)


########################
# 分割字幕部分
########################
def str_to_delta(time_str):
    split = re.split('[:\.]+', time_str)
    microseconds = 0
    hours = int(split[0])
    minutes = int(split[1])
    seconds = int(split[2])
    if len(split) == 4:
        microseconds = int(split[3])
    return timedelta(hours=hours, minutes=minutes, seconds=seconds, microseconds=microseconds)


def delta_to_str(delta):
    time_str = "{0}:{1}:{2}.{3:03d}".format(delta.seconds // 3600, (delta.seconds % 3600) // 60,
                                            delta.seconds % 60, delta.microseconds // 1000)
    return time_str


def find_owner_chapter(in_time_point, in_chapter_list):
    """
    找出一个时间点属于哪个chapter
    return: 返回元组（视频开始时间，视频名称）
    """
    for chapter in in_chapter_list:
        if chapter[0] <= in_time_point < chapter[1]:
            return chapter[0], chapter[2]
    print('No suitable chapter, time-point:{}'.format(in_time_point))
    raise Exception()


def split_subtitles(in_original_sub: str, in_output_root: str, in_chapter_list: list):
    """
    分割字幕文件
    :param in_original_sub: 原始字幕文件
    :param in_output_root: 输出路径根目录
    :param in_chapter_list: 章节列表
    :return:
    """
    in_chapter_list = [(str_to_delta(x[0]), str_to_delta(x[1]), x[2]) for x in in_chapter_list]

    with open(in_original_sub) as orig_sub:
        # 读取头部
        header = []
        for i in range(3):
            header.append(orig_sub.readline())

        # 章节开始时间
        chapter_start_time = None
        # 上一个文件
        last_chapter_name = ''
        # 正在操作的文件
        file_handle = None

        while True:
            line = orig_sub.readline()
            if not line:
                # 如果读到最后一行，关闭正在写入的文件
                if file_handle is not None:
                    file_handle.close()
                break
            line = line.strip()
            if line != '':
                if '-->' in line:  # 此行为时间轴
                    split_line = line.split(' ')
                    start_time = str_to_delta(split_line[0])
                    end_time = str_to_delta(split_line[2])

                    # 本行是时间轴，那么再读入一行，一定是字幕行
                    line_subtitle = orig_sub.readline().strip()

                    # 找出字幕所属视频的名称
                    chapter_start_time, chapter_name = find_owner_chapter(start_time, in_chapter_list)

                    # 创建新文件
                    if chapter_name != last_chapter_name:
                        last_chapter_name = chapter_name
                        # 先关闭之前的文件
                        if file_handle is not None:
                            file_handle.close()

                        sub_file = '{}.vtt'.format(chapter_name)
                        file_handle = open(os.path.join(in_output_root, sub_file), 'w')

                        # 写入头部
                        for l in header:
                            file_handle.write(l)
                        file_handle.write('\n')

                    # 写入时间轴行和字幕行,以及后面的空行

                    # 时间要减去上次最后的时间
                    if chapter_start_time is not None:
                        start_time = start_time - chapter_start_time
                        end_time = end_time - chapter_start_time
                    start_time_str = delta_to_str(start_time)
                    end_time_str = delta_to_str(end_time)

                    file_handle.write(start_time_str)
                    file_handle.write(' ---> ')
                    file_handle.write(end_time_str)
                    file_handle.write('\n{}\n\n'.format(line_subtitle))


if __name__ == '__main__':
    video_file = "D:/Tutorials/PyTorch for Deep Learning/PyTorch for Deep Learning & Machine Learning – Full " \
                 "Course.webm"
    original_sub = "D:/Tutorials/PyTorch for Deep Learning/PyTorch for Deep Learning & Machine Learning – Full " \
                   "Course.en.vtt"
    output_root = 'D:/Tutorials/PyTorch for Deep Learning/Pytorch_For_Deep_Leaning'

    chapter_list = read_chapter_file("D:/Tutorials/PyTorch for Deep Learning/classes.txt")
    chapter_list = add_endtime(chapter_list, video_path=video_file)

    split_video(video_file, output_root, chapter_list)
    split_subtitles(original_sub, output_root, chapter_list)
