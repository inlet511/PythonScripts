# AutoLabelImageTools

## autolabel.py 
自动找出图片中的所有主体，获取其BoundingBox，并返回yolo格式的坐标。
适用于背景相对比较干净，接近白色的图片。

## cleanlabels.py
对比图片目录和标签目录，找出标签目录中已经无效的标签（即在图片目录中没有对应的图片)并删除

## selector.py
在一堆数据中找出一定比例的数据作为验证集或测试集，发送到目标目录中，同时操作图片和标签
