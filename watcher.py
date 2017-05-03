from uploader import *
import sys
def start_watcher(path):

    # set the path to watch as argument, otherwise watch current directory
    if os.path.isdir(path):
        try:
            while True:
                upload_directory(path)
                time.sleep(10)
        # Keyboard Interrupt in pycharm is ctrl-f2
        except KeyboardInterrupt:
            exit()
    else:
        print("Error, path " + path + " is not a valid directory path.")

# start_watcher(sys.argv[1] if len(sys.argv) > 1 else '.')