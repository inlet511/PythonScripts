from autolabel import AutoLabel
from cleanlabels import Cleaner
from selector import Selector
def autolabel():
    tool = AutoLabel('E:/Dev/Panel_Detection/dataset/data/images/train',
                     'E:/Dev/Panel_Detection/dataset/classes.txt',
                     True,
                     'E:/Dev/Panel_Detection/dataset/temp',
                     'E:/Dev/Panel_Detection/dataset/data/labels/train')
    tool.process_all_images()
def cleanlabels():
    cleaner = Cleaner('./images/data/images/train','./images/data/labels/train')
    cleaner.clean_labels()

def select_valid_group():
    selector = Selector('E:/Dev/Panel_Detection/dataset/data/images/train',
                        'E:/Dev/Panel_Detection/dataset/data/labels/train',
                        'E:/Dev/Panel_Detection/dataset/data/images/valid',
                        'E:/Dev/Panel_Detection/dataset/data/labels/valid')
    selector.set_valid_group(0.2)

if __name__== '__main__':
    # autolabel()
    select_valid_group()