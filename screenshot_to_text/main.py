from pynput import *
import pyautogui
import pytesseract
import cv2
import numpy as np
import keyboard
import pyperclip
import re

# 输入参数 **************************
# HoughLineDetection Threshold
LineDetectionThreshold = 40
# HoughLineDetection 直线最小长度
MinLineLength = 100
# HoughLineDetection 间隙大于多少则被认为是两条线
MinLineGap = 20
# 涂抹线条的粗细
LineThickness = 8
# 过滤正则表达式
CleanFilter = r"[|\]\}]"


# Global parameters
start_x, start_y, end_x, end_y = 0,0,0,0

def capture(x1,y1,x2,y2):
    if x2-x1<=0 or y2-y1<=0:
        print("请从左上到右下绘制有效矩形")
        return False
    screenshot = pyautogui.screenshot(region=(x1, y1, x2-x1, y2-y1))
    # 保存截图为临时文件
    screenshot.save('temp.png')
    return True


def remove_chars(input_string, characters_to_remove):
    modified_string = re.sub(characters_to_remove, "", input_string)
    return modified_string


def recognize_numbers():
    image = cv2.imread('temp.png')

    # 将图像转换为灰度
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 高斯滤波降噪
    gaussian = cv2.GaussianBlur(gray_image, (9, 9), 0)
    # 边缘检测
    edges = cv2.Canny(gaussian, 70, 150)
    # cv2.imshow("edges", edges)

    # 使用霍夫线变换检测直线
    lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=LineDetectionThreshold, minLineLength=MinLineLength, maxLineGap=MinLineGap)

    # 如果线条不为空对象
    if not lines is None:
        # 将检测到的线条在图像上标记为白色（255）
        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(image, (x1, y1), (x2, y2), (255, 255, 255), LineThickness)

    # 将标记了线条的图像转换为灰度
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    cv2.imshow("removed_lines", image)
    cv2.waitKey()
    cv2.destroyAllWindows()

    # 使用Tesseract OCR进行数字识别
    result = pytesseract.image_to_string(image, config='--psm 6', lang='eng').strip()
    # 去掉常见的杂乱符号
    clean_result = remove_chars(result,CleanFilter)
    print(clean_result)

    #为粘贴到excel做准备，用制表符分割
    toclipboard = re.sub(r'( )+', r'\t', clean_result)
    pyperclip.copy(toclipboard)



def on_click(x, y, button, pressed):
    global start_x,start_y,end_x,end_y

    # print('{0} at {1}'.format(
    #     'Pressed' if pressed else 'Released',
    #     (x, y)))
    if pressed:
        start_x = x
        start_y = y
    elif keyboard.is_pressed('ctrl'):
        end_x = x
        end_y = y
        cap_result = capture(start_x, start_y, end_x, end_y)
        if cap_result:
            recognize_numbers()
    return True

with mouse.Listener(on_click=on_click) as listen:
    listen.join()
