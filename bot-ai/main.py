import time
import threading
import globals
import config
import signal
import api
from modules import cli, check_image_thread, scan_window_thread
from modules.integration import get_server_id_and_fullname

def handle_signal(signum, frame):
    print('Stopping threads, please wait...')
    globals.threads_stop.set()
    signal.signal(signal.SIGINT, signal.SIG_IGN)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_signal)

    print('Vanguard Bot Tool')

    try:
        cli_result = cli.init()

        config.verbose_errors = cli_result.verbose
        config.config_path = cli_result.config_path

        config.init()

        if not cli_result.immediate_start:
            input('Press enter to continue')

        if not api.init():
            raise Exception('Failed to init API')

        print('Init API success')

        success, globals.game_id, full_server_name = get_server_id_and_fullname(config.server_name)

        if not success:
            raise Exception('Failed to get server')

        print('Successfully found server', full_server_name)

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