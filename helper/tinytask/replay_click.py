"""
复制重放点击操作。 参考 tinyTask

prompt: 使用python 从日志文件中读取每一行日志，根据“2024-01-25 21:36:35,321: Mouse clicked at (1405, 1171) with Button.left” ，解析其中的坐标(1405, 1171) 和 Button.left ， 用pyautogui 按照解析的坐标和左右键，重放鼠标点击
读取日志文件，解析坐标和鼠标按钮，然后使用pyautogui来模拟点击
此脚本会读取日志文件的每一行，使用正则表达式来查找匹配的日志条目，并提取坐标和按钮信息，然后使用pyautogui来模拟鼠标点击。

@since 2024年1月25日 22:07:25 chat-gpt
@since 2024年12月30日 13:22:00 支持点击操作间隔时间重放。增加循环次数设定。
"""
import re
import time
from datetime import datetime
import pyautogui
import logging

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 正则表达式用于匹配日志中的时间戳、坐标和按钮
log_pattern = re.compile(r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}): Mouse clicked at \((\d+), (\d+)\) with (Button\.\w+)")


def parse_and_execute(log_file, loop_count=1, loop_interval=5):
    """
    解析操作日志并重放执行
    @param log_file:
    @param loop_count: 循环次数
    @param loop_interval: 循环间隔
    @return:
    """

    logging.info(f"开始解析日志文件: {log_file}")

    # 读取日志文件并解析每一行
    with open(log_file, 'r') as file:
        lines = file.readlines()

    for loop_index in range(loop_count):
        logging.info(f"开始第 {loop_index + 1} 次循环")
        previous_timestamp = None
        for line in lines:
            match = log_pattern.search(line)
            if match:
                # 提取时间戳、坐标和按钮
                timestamp_str = match.group(1)
                x, y = int(match.group(2)), int(match.group(3))
                button = match.group(4).split('.')[1].lower()  # 'Button.left' -> 'left'

                # 解析时间戳
                current_timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S,%f")

                # 计算时间间隔并sleep
                if previous_timestamp is not None:
                    interval = (current_timestamp - previous_timestamp).total_seconds()
                    logging.info(f"等待 {interval} 秒")
                    time.sleep(interval)

                # 模拟鼠标点击
                logging.info(f"模拟鼠标点击: ({x}, {y}) 按钮: {button}")
                pyautogui.click(x=x, y=y, button=button)

                # 更新前一个时间戳
                previous_timestamp = current_timestamp

        # 循环间隔
        if loop_count > 1:
            logging.info(f"循环间隔 {loop_interval} 秒")
            time.sleep(loop_interval)

    logging.info("日志解析和执行完成")


# 示例调用
parse_and_execute('mouse_log.txt', loop_count=1, loop_interval=5)