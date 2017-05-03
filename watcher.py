from uploader import *
import sys
if __name__ == "__main__":

    # set the path to watch as argument, otherwise watch current directory
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    try:
        while True:
            upload_directory(sys.argv[1])
            time.sleep(10)
    # Keyboard Interrupt in pycharm is ctrl-f2
    except KeyboardInterrupt:
        exit()