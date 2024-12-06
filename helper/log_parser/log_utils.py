import os

"""
日志工具类，抽取公用的方法
@since 2024年12月6日 13:55:09
"""


def get_latest_log_file(directory):
    """
    查找目录中最新的文件
    例如：找到 ~/Downloads 目录下最新下载的日志文件
    @param directory:
    @return:
    """
    log_files = [f for f in os.listdir(directory) if f.endswith('.log')]
    if not log_files:
        return None
    log_files.sort(key=lambda x: os.path.getmtime(os.path.join(directory, x)), reverse=True)
    return log_files[0]


def save_ids_to_file(ids, file_path):
    """
    数组写入到文件中
    @param ids:
    @param file_path:
    @return:
    """
    with open(file_path, 'w') as file:
        for id in ids:
            file.write(f"{id}\n")

