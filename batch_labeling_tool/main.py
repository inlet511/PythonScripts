from autolabel import AutoLabel
from cleanlabels import Cleaner
from selector import Selector
def autolabel():
    tool = AutoLabel('E:/Dev/dataset/panel_dataset/data/images/train',
                     'E:/Dev/dataset/panel_dataset/classes.txt',
                     True,
                     'E:/Dev/dataset/panel_dataset/temp',
                     'E:/Dev/dataset/panel_dataset/data/labels/train')
    tool.process_all_images()
def cleanlabels():
    cleaner = Cleaner('./images/data/images/train','./images/data/labels/train')
    cleaner.clean_labels()

def select_valid_group():
    selector = Selector('./images/data/images/train','./images/data/labels/train','./images/data/images/valid','./images/data/labels/valid')
    selector.set_valid_group(0.3)

if __name__== '__main__':
    autolabel()