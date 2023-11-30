# -*- coding:utf-8 -*-
# 批量生成 ffmpeg 合并需要的文件列表
# @since 2016/8/25

import os

path = '/tmp/foo/'
for m3u8_dir in os.listdir(path):
    if os.path.isdir(os.path.join(path, m3u8_dir)) and m3u8_dir.find('m3u8') != -1:
        content = os.listdir(os.path.join(path, m3u8_dir))
        f = open(os.path.join(path, m3u8_dir, "filelist.txt"), "wb")
        for line in content:
            if line.find('.ts') != -1:
                f.write("file '{}'\n".format(line))
        f.close()

