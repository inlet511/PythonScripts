import numpy as np
import cv2
import os
import argparse

class AutoLabel(object):
    """ 自动给图片添加yolo格式的标签 """

    def __init__(self,
                 image_folder: str,
                 classfile: str = './classes.txt',
                 write_result_image: bool = True,
                 write_image_folder: str = './temp',
                 label_folder: str = './labels'):
        '''
        构造函数
        Args:
            image_folder: 图片文件所在文件夹
            classfile: 类别文本文件
            write_result_image: 是否保存画框图片
            write_image_folder: 画框图片保存路径
            label_folder: 标签文件保存路径
        '''

        self.classfile = classfile
        self.image_folder = image_folder
        self.write_result_image = write_result_image
        self.write_image_folder = write_image_folder
        self.label_folder = label_folder

        # 所有分类
        self.classes = []
        if os.path.exists(self.classfile):
            self.read_classes()
        else:
            raise Exception('Class file({}) doesn\'t exist.'.format(self.image_folder))

    def read_classes(self):
        '''
        设置分类
        :param filename: classes.txt路径
        :return: 无返回值
        '''
        f = open(self.classfile)
        lines = [l.strip('\n') for l in f.readlines()]
        self.classes = lines

    def find_bounding_box(self, image_path):
        '''
        返回图像中主体元素的boundingbox, 格式是Yolo标注的坐标
        :param image_path: 图片路径
        :return: yolo 格式的文本
        '''
        #读取图片并二值化
        img = cv2.imread(image_path)
        height,width,channels = img.shape
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, thresh = cv2.threshold(gray, 120, 255, cv2.THRESH_BINARY_INV)

        # 查找轮廓
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        # 绘制轮廓
        # cv2.drawContours(img, contours, -1, (0,255,0), 3)

        # 对每个轮廓查找bounding box
        bounding_boxes = [cv2.boundingRect(cnt) for cnt in contours]
        # 由(x,y,w,h)的形式转换为(x1,y1,x2,y2)的形式
        bounding_rectagles = [(box[0],box[1],box[0]+box[2],box[1]+box[3]) for box in bounding_boxes]

        # 找到左上的最小值和右下的最大值，即得到最外层边框
        np_bb = np.array(bounding_rectagles)
        max_arr = np.amax(np_bb,axis=0)
        min_arr = np.amin(np_bb,axis=0)
        out_bound = [min_arr[0],min_arr[1],max_arr[2],max_arr[3]]

        # 对比文件名称和标签名称，确定标签分类
        _, filename = os.path.split(image_path)
        filename, ext = os.path.splitext(filename)
        first_part = filename.split('_')[0]
        if first_part in self.classes:
            class_index = self.classes.index(first_part)
        else:
            raise Exception('Image({}) Not in class list.'.format(filename))

        # 输出图片作为对照
        if self.write_result_image:
            output = cv2.rectangle(img, (out_bound[0], out_bound[1]), (out_bound[2], out_bound[3]), (0, 0, 255), 2)
            new_filename = r"{n}_box{e}".format(n=filename,e=ext)
            if not os.path.exists(self.write_image_folder):
                os.makedirs(self.write_image_folder)
            write_image_path = os.path.join(self.write_image_folder,new_filename)
            cv2.imwrite(write_image_path,output)

        yolo_txt = '{idx} {x} {y} {w} {h}'.format(idx=class_index,
                                                  x=(out_bound[0]+out_bound[2])*0.5/width,
                                                  y=(out_bound[1]+out_bound[3])*0.5/height,
                                                  w=(out_bound[2]-out_bound[0])/width,
                                                  h=(out_bound[3] - out_bound[1])/height)
        return yolo_txt

    def process_all_images(self):
        '''
        处理所有的图片
        :return:
        '''
        if not os.path.exists(self.image_folder):
            raise Exception('Image Folder({}) doesn\t exist'.format(self.image_folder))
        if not os.path.exists(self.label_folder):
            os.makedirs(self.label_folder)

        current_file_idx=0
        for root,dirs,files in os.walk(self.image_folder):
            total_count = len(files)
            for fileName in files:
                current_file_idx += 1
                print("Handling file {name} \t [{idx}/{total}]".format(name=fileName,idx=current_file_idx,total=total_count))
                _, ext = os.path.splitext(fileName)
                if(ext in ['.jpg','.png']):
                    filePath = os.path.join(root,fileName)

                    # 寻找边框
                    yolo_txt = self.find_bounding_box(filePath)

                    name_part, _ = os.path.splitext(fileName)
                    label_file_name = '{}.txt'.format(name_part)
                    label_file_fullname = os.path.join(self.label_folder,label_file_name)
                    with open(label_file_fullname,'w') as f:
                        f.write(yolo_txt)



if __name__== '__main__':
    parser = argparse.ArgumentParser(description='自动给图片添加yolo格式的标签')
    parser.add_argument('--img_folder', '-i', help='图片文件所在文件夹', required=True)
    parser.add_argument('--class_file', '-c', help='类别文本文件', required=True)
    parser.add_argument('--save_img', '-s', help='是否保存画框图片', required=True)
    parser.add_argument('--save_folder', '-f', help='画框图片保存路径', required=True)
    parser.add_argument('--label_folder', '-l', help='标签文件保存路径', required=True)

    args = parser.parse_args()

    autolabel = AutoLabel(args.img_folder, args.class_file, args.save_img, args.save_folder, args.label_folder)
    autolabel.process_all_images()