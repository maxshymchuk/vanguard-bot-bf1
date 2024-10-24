import time
import threading
import globals
import signal
import pytesseract
from modules.image_checker import check_image_thread
from modules.window_scanner import scan_window_thread

pytesseract.pytesseract.tesseract_cmd = './tesseract/tesseract.exe'

def handle_signal(signum, frame):
    print('Stopping threads, please wait...')
    globals.threads_stop.set()
    signal.signal(signal.SIGINT, signal.SIG_IGN)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_signal)
    thread1 = threading.Thread(target=scan_window_thread)
    thread2 = threading.Thread(target=check_image_thread)
    thread1.start()
    thread2.start()
    try:
        while not globals.threads_stop.is_set():
            time.sleep(1)
        thread1.join()
        thread2.join()
    except Exception as e:
        print(f'Unexpected error: {e}')
    finally:
        print('Program terminated')