import os
from random import sample
import shutil
import argparse

class Selector(object):
    """
    随机抽取一定比例的数据作为验证集或测试集
    """
    def __init__(self,
                 image_folder: str,
                 label_folder: str,
                 target_image_folder: str,
                 target_label_folder: str):
        '''
        :param image_folder: 图片所在目录
        :param label_folder: 标签所在目录
        :param target_image_folder: 目标图片所在目录
        :param target_label_folder: 目标标签所在目录
        '''
        self.image_folder = image_folder
        self.label_folder = label_folder
        self.target_image_folder = target_image_folder
        self.target_label_folder = target_label_folder

        # 图片文件列表
        self.img_paths = []
        # 标签文件列表
        self.lbl_paths = []

        if not os.path.exists(image_folder):
            raise Exception("Image folder ({}) doesn't exist".format(image_folder))
        if not os.path.exists(label_folder):
            raise Exception("Label folder ({}) doesn't exist".format(label_folder))

        if not os.path.exists(target_image_folder):
            try:
                os.makedirs(target_image_folder)
            except IOError:
                print("Error, Create folder failed.")
            else:
                print("Target Image folder doesn't exist, created one. Path:{}".format(target_image_folder))

        if not os.path.exists(target_label_folder):
            try:
                os.makedirs(target_label_folder)
            except IOError:
                print("Error, Create folder failed.")
            else:
                print("Target label folder doesn't exist, created one. Path:{}".format(target_label_folder))

        # 构建文件列表
        for root, dirs, files in os.walk(self.image_folder):
            for file in files:
                self.img_paths.append(os.path.join(root,file))

        for root, dirs, files in os.walk(self.label_folder):
            for file in files:
                self.lbl_paths.append(os.path.join(root, file))

        if len(self.img_paths) != len(self.lbl_paths):
            raise Exception("Image count and label count doesn't match, please check")

    def set_valid_group(self, percent:float=0.3):
        count = len(self.img_paths)
        select_count = round(percent * count)
        indices = list(range(count))
        select_indices = sample(indices, select_count)

        # 转移文件到目标位置
        for idx in select_indices:
            try:
                shutil.move(self.img_paths[idx], self.target_image_folder)
                print("Moving file: {}".format(self.img_paths[idx]))
                shutil.move(self.lbl_paths[idx], self.target_label_folder)
                print("Moving file: {}".format(self.lbl_paths[idx]))
            except IOError:
                print("Error when trying to move files")

        print("Finished moving files.")

if __name__== '__main__':
    parser = argparse.ArgumentParser(description='随机抽取一定比例的数据作为验证集或测试集')
    parser.add_argument('--select_percentage', '-p', help='选择的百分比，以小数表示', required=True)
    parser.add_argument('--image_folder', '-i', help='图片所在目录', required=True)
    parser.add_argument('--label_folder', '-l', help='标签所在目录', required=True)
    parser.add_argument('--target_image_folder', '-ti', help='目标图片所在目录', required=True)
    parser.add_argument('--target_label_folder', '-tl', help='目标标签所在目录', required=True)


    args = parser.parse_args()

    tool = Selector(args.image_folder, args.label_folder, args.target_image_folder, args.target_label_folder)
    tool.set_valid_group(float(args.select_percentage))