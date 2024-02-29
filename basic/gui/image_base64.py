import base64

"""
将图片转换为Base64编码的字符串
https://imgonline.tools/zh/image-to-base64 
@since 2024年2月29日 11:47:54
"""

# 图片文件路径
image_path = 'Snipaste_2024-02-29_10-23-55.png'

# 读取图片文件并转换为Base64编码
with open(image_path, 'rb') as image_file:
    encoded_string = base64.b64encode(image_file.read())

# 如果你需要将Base64编码的字符串解码为原始的二进制数据
# decoded_image_data = base64.b64decode(encoded_string)

# Base64图像源:data:image/png;base64, + 如下Base64编码的字符串
# 打印或使用Base64编码的字符串
print(encoded_string)