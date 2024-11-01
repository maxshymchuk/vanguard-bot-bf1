import time
import threading
import config.overlay
import globals
import config
import api
import signal
import warnings
# This is not ideal but ImageAI generates a few long warnings that we can't do much about so suppress them...
warnings.simplefilter('ignore', UserWarning)
warnings.simplefilter('ignore', FutureWarning)
import models
from modules import check_image_thread, scan_window_thread
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

        if cli_result.config_path:
            config.config_path = cli_result.config_path

        config_manager = config.init()

        if not config_manager.is_all_positions_set:
            coordinate_strs = ['next player', 'third person view']
            box_strs = ['player name area', 'weapon icon area', 'weapon name area']
            configoverlay = config.overlay.ConfigOverlay(coordinate_strs, box_strs)
            success, coordinates, boxes = configoverlay.execute_setup()
            if success:
                print('Config set')
                config.change_player_button_coordinate = coordinates[0]
                config.third_person_view_button_coordinate = coordinates[1]
                config.player_name_box = boxes[0]
                config.weapon_icon_box = boxes[1]
                config.weapon_name_box = boxes[2]
            else:
                print('Failed to set config, exiting')
                quit()
            config_manager.save()

        if not cli_result.immediate_start:
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