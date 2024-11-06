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
from modules.integration import get_server_id_and_fullname, get_players

def handle_signal(signum, frame):
    print('Stopping threads, please wait...')
    globals.threads_stop.set()
    signal.signal(signal.SIGINT, signal.SIG_IGN)

if __name__ == '__main__':
    signal.signal(signal.SIGINT, handle_signal)
    print('Vanguard Bot Tool')

    try:
        cli_result = cli.init()

        config.verbose = cli_result.verbose
        config.should_save_screenshot = cli_result.screenshot

        if cli_result.config_path:
            config.config_path = cli_result.config_path

        config_manager = config.init()

        should_test_config = False
        if not config_manager.is_all_positions_set or cli_result.resetup:
            box_strs = ['player name area', 'weapon icon area', 'weapon name area', 'secondary weapon name area', 'gadget slot 1 area', 'gadget slot 2 area']
            input('Press enter to begin setup')
            config_overlay = config.overlay.ConfigOverlay(box_strs)
            success, boxes = config_overlay.execute_setup()
            if success:
                print('Config set')
                config.player_name_box, config.weapon_icon_box, config.weapon_name_box, config.weapon_name_slot2_box, \
                    config.gadget_slot_1_box, config.gadget_slot_2_box = boxes
                should_test_config = input('Test config? Y/N ').upper() == 'Y'
            else:
                print('Setup config terminated, exiting')
                quit()
            config_manager.save()

        if should_test_config or cli_result.test_config:
            print(f'Taking screenshots of the next three players, please wait a few seconds then confirm results in {config.screenshots_path}')
            config.overlay.test_overlay()

        if not cli_result.immediate_start:
            input('Press enter to continue')

        print('Fetching API details...', end = ' ')

        success, persona_name = api.init()
        if not success:
            raise Exception('Failed to init API')

        print('Success')

        print('You are', persona_name)

        print('Fetching server information...', end = ' ')

        success, globals.game_id, full_server_name = get_server_id_and_fullname(config.server_name)

        if not success:
            raise Exception('Failed to get server')

        success, globals.teams = get_players()

        if not success:
            raise Exception('Failed to get server teams')

        print('Success')

        print(f'Found server {full_server_name}')

        models.load_model()

        thread1 = threading.Thread(target = scan_window_thread, daemon = True)
        thread2 = threading.Thread(target = check_image_thread, daemon = True)
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