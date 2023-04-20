import numpy as np
import cv2
import time


if __name__ == '__main__':
    img_rgb = cv2.imread('images/dcs01.png')  # 需要检测的图片
    img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)  # 转化成灰色
    template_img = cv2.imread('images/item02.png', 0)  # 模板小图

    begin_time = time.time()

    h,w = template_img.shape[:2]

    result = cv2.matchTemplate(img_gray, template_img, cv2.TM_CCORR_NORMED)

    threshold = 0.98
    loc = np.where( result > threshold)

    mask = np.zeros(img_rgb.shape[:2], np.uint8)

    detection_count = 0
    detections=[]
    for pt in zip(*loc[::-1]):
        if mask[pt[1]+int(round(h/2)), pt[0]+int(round(w/2))] != 255:
            detection_count +=1
            mask[pt[1]:pt[1]+h, pt[0]:pt[0]+w] = 255
            detections.append((pt[0],pt[1],pt[0]+w,pt[1]+h))
            cv2.rectangle(img_rgb, pt, (pt[0]+w, pt[1]+h), (0,0,255), 1)

    time_spent = time.time() - begin_time
    print("detection cost: ",time_spent," ms")
    print("detection count:", detection_count)
    print("detection boxes:", detections)

    cv2.imshow("result",img_rgb)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




