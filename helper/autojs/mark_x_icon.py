import cv2
import numpy as np

"""
使用OpenCV识别图片中的关闭按钮（通常是一个“X”符号）。
模板匹配：如果有一个已知的关闭按钮图像，可以使用模板匹配来找到相似的区域。

缺点： 如果遇到图片翻转、缩放，就不能识别。

@since 2024年4月7日 15:09:58
"""

def find_close_button(image_path, template_path, threshold=0.6):
    # 读取图片和模板
    image = cv2.imread(image_path)
    gray_template = cv2.imread(template_path, 0)  # 模板应该是灰度图

    # 由于是灰度图像，image.shape 将只返回两个值，分别是高度和宽度。
    # 如果是彩色图像，image.shape 会返回三个值，分别是高度、宽度和通道数。
    w, h = gray_template.shape[:2]

    # 将图片转换为灰度图
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 保存灰度图像 size: 11K --> 6K
    # cv2.imwrite('gray_image.png', gray_image)

    # 应用模板匹配
    res = cv2.matchTemplate(gray_image, gray_template, cv2.TM_CCOEFF_NORMED)

    # 获取匹配结果大于阈值的位置
    loc = np.where(res >= threshold)

    # 标记匹配区域
    for pt in zip(*loc[::-1]):
        cv2.rectangle(image, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)

    # 显示结果
    cv2.imshow('Detected', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # 使用示例
    find_close_button('Snipaste_2024-04-07_14-36-24.png', 'x_icon.png')
