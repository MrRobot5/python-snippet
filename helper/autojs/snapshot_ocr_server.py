import base64
import numpy as np
from io import BytesIO
from PIL import Image

from flask import Flask, request
from paddleocr import PaddleOCR


"""
启动一个简单的HTTP服务器并处理 autojs 的POST请求。
usage: 
python snapshot_ocr_server.py
curl http://127.0.0.1:5000/handle/say

curl -X POST -F "key=value1" -F "file=@/d/1.png" http://127.0.0.1:5000/handle/ocr

pip install flask

@since 2024年3月26日 20:13:22
"""

app = Flask(__name__)
ocr = PaddleOCR(use_angle_cls=True, lang="ch")


@app.route('/handle/say', methods=['GET'])
def handle_say():
    """
    服务探测
    @return: "Hello, Guest!"
    """
    # name = request.form.get('name')  # 获取POST表单数据中的'name'
    name = request.args.get('name', 'Guest')
    print(f"Name: {name}")
    return f"Hello, {name}!", 200

@app.route('/handle/ocr', methods=['POST'])
def handle_ocr():
    """
    对截图图片文字识别，返回识别坐标
    @return: [
                {
                    "bounds": {
                        "bottom": 42,
                        "left": 15,
                        "right": 148,
                        "top": 19
                    },
                    "text": "姓名：张**"
                }
            ]
    @since 2024年3月27日 17:25:47
    """
    if 'file' not in request.files:
        return 'No file part in the request'

    file = request.files['file']
    # Image.open函数来打开上传的文件
    img = Image.open(file)
    # 将PIL图像转换为ndarray
    img_array = np.array(img)
    result = scan(img_array)

    # 获取其他的表单数据
    form_data = request.form['key']

    return result


def scan(img_array):
    result = ocr.ocr(img_array, cls=False)
    ocr_res = []
    for idx in range(len(result)):
        res = result[idx]
        for line in res:
            ocr_res.append({
                "text": line[1][0],
                "bounds": box_to_rect(line[0]),
            })

    print(ocr_res)
    return ocr_res


def base64_to_nparray(base64_image):
    """
    @param base64_image: 包含base64编码图像的字符串
    @return: 包含图像数据的ndarray
    """

    # 从base64字符串解码图像数据
    image_data = base64.b64decode(base64_image)

    # 将图像数据转换为PIL图像
    image = Image.open(BytesIO(image_data))

    # 将PIL图像转换为ndarray
    return np.array(image)


def box_to_rect(box):
    """
    bounds box 坐标集合转为 Rect 坐标 left top right, bottom
    @param box [[2.0, 48.0], [246.0, 50.0], [246.0, 69.0], [2.0, 67.0]]
    @return: rect
    @since 2024年3月27日 15:16:55
    """
    left = box[0][0]
    top = box[0][1]
    right = box[2][0]
    bottom = box[2][1]

    result = {
        "left": left,
        "top": top,
        "right": right,
        "bottom": bottom
    }

    # print(f"Left: {left}, Top: {top}, Right: {right}, Bottom: {bottom}")
    return result


if __name__ == '__main__':
    # app.run(debug=True)
    app.run()
