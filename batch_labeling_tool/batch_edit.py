import os

folder = r'E:/Dev/PanelDataSample/025cc_p1_lbl'

# 修改一个文件夹中的所有文件，将前两个文字改为16
def edit(folder):
    for root, dirs, files in os.walk(folder):
        for file in files:
            filename = os.path.join(root, file)
            with open(filename, "r+") as f:
                content = list(f.readline())
                content[:2] =['1','6']
                f.seek(0)
                f.write(''.join(content))


if __name__ == '__main__':
    edit(folder)