# -*- coding:utf-8 -*-

"""
    图片文本识别
    两种实现方式：
    1. 自己手动实现，自定义识别算法
        参考： https://www.cnblogs.com/hearzeus/p/5226546.html

        高级算法参考： http://nladuo.github.io/2018/12/08/%E9%82%A3%E4%BA%9B%E5%B9%B4%EF%BC%8C%E6%88%91%E7%88%AC%E8%BF%87%E7%9A%84%E5%8C%97%E7%A7%91-%E5%85%AB-%E2%80%94%E2%80%94%E5%8F%8D%E5%8F%8D%E7%88%AC%E8%99%AB%E4%B9%8B%E9%AA%8C%E8%AF%81%E7%A0%81%E8%AF%86%E5%88%AB/?utm_source=tuicool&utm_medium=referral

    2. 现有的lib, https://pypi.org/project/pytesseract/
        INSTALLATION:
        You will need the Python Imaging Library (PIL)
        Install Google Tesseract OCR
        pip install pytesseract

        参考： https://sourceforge.net/projects/tesseract-ocr-alt/

"""
import urllib2
from PIL import Image
import cStringIO
import pytesseract


def download_image():
    getCode_url = "http://xjzw.th28.cn/default_pay_template/images/yzm.jsp?0.7855853862762292"
    header = {"Referer": "http://xjzw.th28.cn/codeinfoAction!verifygc", 'Cache-Control': "max-age=0"}
    # header['Host']="icp.alexa.cn"
    # header['User-Agent']="Mozilla/5.0 (Windows NT 6.3; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0"
    request = urllib2.Request(getCode_url, headers=header)
    res = urllib2.urlopen(request).read()
    image = Image.open(cStringIO.StringIO(res))
    image.show()


def crop_image(out, index):
    if index == 1:
        region = (3, 3, 16, 17)
        result = out.crop(region)
        return result
    elif index == 2:
        region = (17, 3, 28, 17)
        result = out.crop(region)
        return result
    elif index == 3:
        region = (30, 3, 41, 17)
        result = out.crop(region)
        return result
    else:
        region = (43, 3, 55, 17)
        result = out.crop(region)
        return result


def parse_image():
    image = Image.open("/tmp/captchas/5ec4f274-fda2-4583-9eea-e819a399b07a.bmp")
    # 1. 转为灰度图
    imgry = image.convert("L")
    # imgry.show()

    # 2. 二值化
    # threshold = 150 这个是一个阈值，具体是多少，看情况，如果比较专业的可以根据图片的灰度直方图来确定
    threshold = 150
    table = []
    for i in range(256):
        if i < threshold:
            table.append(0)
        else:
            table.append(1)
    out = imgry.point(table, '1')
    # out.show()

    # 3. 图片裁剪
    image1 = crop_image(out, 1)
    # image1.show()
    image2 = crop_image(image, 2)
    image3 = crop_image(image, 3)
    image4 = crop_image(image, 4)

    # 4. 提取特征值


def tesseract():
    # If you don't have tesseract executable in your PATH, include the following:
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract'
    print(pytesseract.image_to_string(Image.open("/tmp/captchas/8d7d3288-5994-46fb-a7b5-64b1d8ca8c84.bmp")))


tesseract()

# download_image()
# parse_image()
