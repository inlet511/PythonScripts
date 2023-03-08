import os
import argparse

class Cleaner(object):
    """
    清理无用的标签(图片已经不在的标签)
    """

    def __init__(self,
                 image_folder: str,
                 label_folder: str):
        """
        :param image_folder: 图片所在目录
        :param label_folder: 标签所在目录
        """
        self.image_folder = image_folder
        self.label_folder = label_folder

        # 名称列表(不含扩展名)
        self.img_names_noext = []
        # 要删除的标签文件路径列表
        self.labels_to_delete = []

        if not os.path.exists(image_folder):
            raise Exception("Image folder ({}) doesn't exist".format(image_folder))
        if not os.path.exists(label_folder):
            raise Exception("Label folder ({}) doesn't exist".format(label_folder))

        # 构建名称列表
        for root, dirs, files in os.walk(self.image_folder):
            for file in files:
                filename, _ = os.path.splitext(file)
                self.img_names_noext.append(filename)

    def clean_labels(self):
        # 标记要删除的标签文件
        for root, dirs, files in os.walk(self.label_folder):
            for file in files:
                n, _ = os.path.splitext(file)
                if not n in self.img_names_noext:
                    self.labels_to_delete.append(os.path.join(root, file))
        # 执行删除
        for f in self.labels_to_delete:
            os.remove(f)
            print("Removed:{}".format(f))

        if len(self.labels_to_delete) == 0:
            print("No labels need to be deleted")
        # 清理删除列表
        self.labels_to_delete.clear()

if __name__== '__main__':
    parser = argparse.ArgumentParser(description='清理无用的标签(图片已经不在的标签)')
    parser.add_argument('--image_folder', '-i', help='图片所在目录', required=True)
    parser.add_argument('--label_folder', '-l', help='标签所在目录', required=True)
    args = parser.parse_args()

    tool = Cleaner(args.image_folder, args.label_folder)
    tool.clean_labels()