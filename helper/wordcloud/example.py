# -*- coding:utf-8 -*-
"""
    生成词云

    参考： https://ask.hellobi.com/blog/python_shequ/18705

    设置全局源地址
    pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple

    pip install matplotlib
        Matplotlib strives to produce publication quality 2D graphics
    pip install jieba

    pip install wordcloud

      问题：默认支持python 3.x，需要下载安装包，手动安装
      pip install wordcloud matplotlib-1.5.0-cp27-none-win_amd64.whl
      https://sourceforge.net/projects/matplotlib/files/matplotlib/matplotlib-1.5.0/windows/
      问题：xxx is not a supported wheel on this platform.
      注意查看python 的版本和 cpu位数(x86 x64)

"""

import jieba
from wordcloud import WordCloud
# from scipy.misc import imread

# 读取文本文件
text = open('word_cloud_demo.log', 'r', encoding='UTF-8').read()
# 对文本进行分词
# cut分词，然后将分开的词用空格连接
cut_text = ' '.join(jieba.cut(text))
# 读取图片
# color_mask = imread('/tmp/background.jpg')
# 生成词云
font = 'C:\Windows\Fonts\simhei.ttf'
cloud = WordCloud(font_path=font, width=800, height=600, background_color="white", max_words=300, max_font_size=80)
cloud.generate(cut_text)

# 保存文件
cloud.to_file('word_cloud.png')
