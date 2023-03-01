import os
import argparse
from collections import defaultdict
import hashlib
import collections

size_files_dict= defaultdict(list)

def create_hash_md5(path, blocksize=4096):
    '''
    :param path: 文件路径
    :param blocksize: 每次读取的块的大小
    :return: 文件的md5哈希值
    '''
    # 初始化一个md5 hash
    hash = hashlib.md5()
    with open(path,'rb') as file:
        # 一次读取blocksize字节的文件，并更新hash值,直到退出
        while True:
            block = file.read(blocksize)
            if not block:
                break
            # hash.update 接收新增加内容，并更新hash
            hash.update(block)
    return hash.hexdigest()


def find(folder:str):
    if not os.path.exists(folder):
        raise Exception("文件夹不存在")

    # 查找大小相同的文件
    for root, dirs, files in os.walk(folder):
        for file in files:
            f = os.path.join(root, file)
            size = os.path.getsize(f)
            size_files_dict[size].append(f)

    keys = list(size_files_dict.keys())
    for key in keys:
        # 如果多于一个，说明有文件大小相同的，继续检查
        if len(size_files_dict[key]) > 1:
            # same_size_files 是 [‘file1','file2'...] 的形式
            same_size_files = size_files_dict[key]
            # md5s 是 same_size_files 逐个对应位置的文件 计算出来的md5值
            md5s = []
            # 创建md5列表
            for f in same_size_files:
                hash = create_hash_md5(f)
                md5s.append(hash)
            # 查看md5列表中相同的元素
            c = dict(collections.Counter(md5s))

            # s 表示数量大于1的md5列表
            s = [k for k,v in c.items() if v > 1]
            if len(s)>0: # s有可能为空，仍需这个判断
                # 有相同值(s[0])的md5在md5s中的索引列表
                indices = [ i for i,val in enumerate(md5s) if val==s[0]]
                print("[File Size:{filesize} ] Same files:-------------------".format(filesize=key))
                samefiles = [val for idx, val in enumerate(same_size_files) if idx in indices]
                for i in samefiles:
                    print(i)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder', '-f', help='要查找的目录', required=True)
    args = parser.parse_args()
    find(args.folder)



