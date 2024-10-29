import time
import threading
import globals
import config
import signal
import pytesseract
from api import init_api
from modules import check_image_thread, scan_window_thread
from modules.integration import get_server_id_and_fullname

pytesseract.pytesseract.tesseract_cmd = './tesseract/tesseract.exe'

def handle_signal(signum, frame):
    print('Stopping threads, please wait...')
    globals.threads_stop.set()
    signal.signal(signal.SIGINT, signal.SIG_IGN)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_signal)

    print('Vanguard Bot Tool')

    try:
        args = globals.parser.parse_args()
        print(args)
        if 'config' in args:
            config.should_read_config = args.config
        if 'verbose' in args:
            config.verbose_errors = args.verbose
    except:
        pass

    print(f'Use config? {config.should_read_config}')
    print(f'Verbose API errors? {config.verbose_errors}')

    try:
        if not init_api():
            raise Exception('Failed to init API')

        print('Init API success')

        servername = '![VG]Vanguard'
        success, globals.game_id, fullservername = get_server_id_and_fullname(servername)

        if not success:
            raise Exception('Failed to get server')

        print('Successfully found server ' + fullservername)

        thread1 = threading.Thread(target=scan_window_thread)
        thread2 = threading.Thread(target=check_image_thread)
        thread1.start()
        thread2.start()
        while not globals.threads_stop.is_set():
            time.sleep(1)
        thread1.join()
        thread2.join()
    except Exception as e:
        print(f'Unexpected error: {e}')
    finally:
        print('Program terminated')