import sys
import time
import logging
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
from uploader import *

class MyHandler(FileSystemEventHandler):
    # cannot use on_any_event because we do not want to fire off when file deleted
    def on_created(self, event):
        print(time.asctime() + " | " + os.path.abspath(event._src_path) + ' ' + event.event_type + '.')
        if event.is_directory:
            upload_directory(event._src_path)
        else:
            upload_file(event._src_path)

    def on_modified(self, event):
        print(time.asctime() + " | " + os.path.abspath(event._src_path) + ' ' + event.event_type + '.')
        if event._src_path == sys.argv[1]:
            return
        if event.is_directory:
            upload_directory(event._src_path)
        else:
            upload_file(event._src_path)

    def on_moved(self, event):
        print(time.asctime() + " | " + os.path.abspath(event._src_path) + ' ' + event.event_type + '.')
        if event.is_directory:
            upload_directory(event._src_path)
        else:
            upload_file(event._src_path)

if __name__ == "__main__":

    # set the path to watch as argument, otherwise watch current directory
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            time.sleep(1)
    # Keyboard Interrupt in pycharm is ctrl-f2
    except KeyboardInterrupt:
        observer.stop()
    observer.join()