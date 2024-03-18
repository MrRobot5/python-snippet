from PIL import Image, ImageDraw, ImageFont

"""
要使用Python处理图片并将其分为3列和4行的区域，你可以使用Pillow库（PIL的一个分支）
每个区域内标注出对应的图片宽度和高度的比例，

@since 2024-03-18 20:50:16 chat-gpt
"""


# 打开图片
image_path = 'your_image.jpg'  # 替换为你的图片路径
image = Image.open(image_path)

# 获取图片尺寸
width, height = image.size

# 创建一个ImageDraw对象
draw = ImageDraw.Draw(image)

# 指定字体和大小
font = ImageFont.truetype('arial.ttf', size=16)

# 计算每列和每行的宽度和高度
col_width = width / 3
row_height = height / 4

# 画红色的列线和行线，并标注比例
for i in range(1, 3):
    x = i * col_width
    draw.line((x, 0, x, height), fill='red', width=2)

for i in range(1, 4):
    y = i * row_height
    draw.line((0, y, width, y), fill='red', width=2)

# 标注每个区域的宽度和高度比例
for i in range(3):
    for j in range(4):
        # 计算区域的中心点
        x_center = (i + 0.5) * col_width
        y_center = (j + 0.5) * row_height
        # 创建比例文本
        text = f"{(i+1)/3:.2f}, {(j+1)/4:.2f}"
        # 获取文本大小
        # text_width, text_height = font.getsize(text)
        text_width, text_height = 10, 10
        # 计算文本位置
        text_x = x_center - text_width / 2
        text_y = y_center - text_height / 2
        # 在区域中心绘制文本
        draw.text((text_x, text_y), text, fill='red', font=font)

# 保存或显示修改后的图片
image.save('marked_image.jpg')  # 保存到新文件
image.show()  # 直接显示图片
