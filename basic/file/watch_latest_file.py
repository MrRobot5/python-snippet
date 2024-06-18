import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

"""
监听目录中的最新文件，并检查其内容是否包含特定关键字。

这个脚本的工作原理如下：
1.使用watchdog库来监听指定目录的变化。
2.每当目录中的文件被创建或修改时，FileHandler类的on_modified或on_created方法会被调用。
3.check_latest_file方法会查找目录中的最新文件，并检查其内容是否包含关键字"无数据"。
4.如果检测到关键字，脚本会停止执行。

pip install watchdog

@since 2024年6月18日 15:41:14
"""

class FileHandler(FileSystemEventHandler):
    def __init__(self, directory):
        self.directory = directory
        self.latest_file = None

    def on_modified(self, event):
        if event.is_directory:
            return
        self.check_latest_file()

    def on_created(self, event):
        if event.is_directory:
            return
        self.check_latest_file()

    def check_latest_file(self):
        files = [os.path.join(self.directory, f) for f in os.listdir(self.directory)]
        files = [f for f in files if os.path.isfile(f) and f.endswith('.json')]
        if not files:
            return
        latest_file = max(files, key=os.path.getmtime)
        if latest_file != self.latest_file:
            self.latest_file = latest_file
            print(f"New latest file detected: {self.latest_file}")
            self.check_file_content()

    def check_file_content(self):
        with open(self.latest_file, 'r', encoding='utf-8') as file:
            content = file.read()
            if "无数据" in content:
                print("Detected '无数据' in the latest file. Stopping execution.")
                observer.stop()

if __name__ == "__main__":
    directory_to_watch = "/export/data"

    event_handler = FileHandler(directory_to_watch)
    observer = Observer()
    observer.schedule(event_handler, directory_to_watch, recursive=False)
    observer.start()

    try:
        while observer.is_alive():
            observer.join(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
