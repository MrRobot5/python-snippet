

"""
AutoJs 标识并验证关闭按钮。
工具优势：
网络传输 替代 设备文件互相拷贝（snapshot、 x_icon）


操作步骤：
1. 使用 helper/autojs/snapshot_ocr_server.py 上传广告 snapshot image
2. 截取关闭按钮 icon, rename x_icon.png
3. 使用 basic/ocr/mark_x_icon.py 验证识别有效性。
4. 使用 base64 加工为字符串。
5. 配置到 commons x_icon_config, 生产环境使用。

const x_icon_config = {
  "baidu_reward_close_icon": "base64"

}
let base64 = x_icon_config["baidu_reward_close_icon"]

"""

