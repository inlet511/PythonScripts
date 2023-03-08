from autolabel import AutoLabel
from cleanlabels import Cleaner
from selector import Selector
def autolabel():
    tool = AutoLabel('./images/data/images/train','./classes.txt',True,'./train_result','./images/data/labels/train')
    tool.process_all_images()
def cleanlabels():
    cleaner = Cleaner('./images/data/images/train','./images/data/labels/train')
    cleaner.clean_labels()

def select_valid_group():
    selector = Selector('./images/data/images/train','./images/data/labels/train','./images/data/images/valid','./images/data/labels/valid')
    selector.set_valid_group(0.3)

if __name__== '__main__':
    cleanlabels()
    select_valid_group()