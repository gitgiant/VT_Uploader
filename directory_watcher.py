import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import platform
import os
from uploader import *

class MyHandler(FileSystemEventHandler):
    # cannot use on_any_event because we do not want to fire off when file deleted
    def on_created(self, event):
        if event.is_directory:
            upload_directory(event._src_path)
        else:
            upload_file(event._src_path)

    def on_modified(self, event):
        if event.is_directory:
            upload_directory(event._src_path)
        else:
            upload_file(event._src_path)

    def on_moved(self, event):
        if event.is_directory:
            upload_directory(event._src_path)
        else:
            upload_file(event._src_path)
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    # set the path to watch as argument, otherwise watch current directory
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
        else:
            print("Got it")
    # Keyboard Interrupt in pycharm is ctrl-f2
    except KeyboardInterrupt:
        observer.stop()
    observer.join()