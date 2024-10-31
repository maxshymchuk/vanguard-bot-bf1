import time
import threading
import globals
import config
import api
import signal
import warnings
# This is not ideal but ImageAI generates a few long warnings that we can't do much about so suppress them...
warnings.simplefilter('ignore', UserWarning)
warnings.simplefilter('ignore', FutureWarning)
import models
from modules import init, check_image_thread, scan_window_thread
from modules.integration import get_server_id_and_fullname
from modules.recognition import recognize_text

def handle_signal(signum, frame):
    print('Stopping threads, please wait...')
    globals.threads_stop.set()
    signal.signal(signal.SIGINT, signal.SIG_IGN)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_signal)
    print('Vanguard Bot Tool')

    immediate_start = init()

    try:
        print(f'Use config? {config.should_read_config}')
        print(f'Verbose API errors? {config.verbose_errors}')
        print(f'Save screenshots? {config.should_save_screenshots}')

        if not immediate_start:
            input('Press enter to continue')

        if not api.init():
            raise Exception('Failed to init API')

        print('Init API success')

        success, globals.game_id, full_server_name = get_server_id_and_fullname(config.server_name)

        if not success:
            raise Exception('Failed to get server')

        print('Successfully found server', full_server_name)

        models.load_model()

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