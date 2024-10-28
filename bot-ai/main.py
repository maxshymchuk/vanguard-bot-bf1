import time
import threading
import globals
import signal
import pytesseract
from modules.image_checker import check_image_thread
from modules.window_scanner import scan_window_thread
from modules.bf1api_integration import _search_for_and_kick_player
from bf1api.main import init_api, get_server_id_and_fullname
from discord import utils as discordutils

pytesseract.pytesseract.tesseract_cmd = './tesseract/tesseract.exe'

def handle_signal(signum, frame):
    print('Stopping threads, please wait...')
    globals.threads_stop.set()
    signal.signal(signal.SIGINT, signal.SIG_IGN)

if __name__ == '__main__':

    if not init_api(True):
        raise Exception('Failed to init API')
    
    servername = '![VG]Vanguard'
    success, globals.gameID, fullservername = get_server_id_and_fullname(servername)

    if not success:
        raise Exception('Failed to get server')
    else:
        print('Successfully found server ' + fullservername)
    
    # #teams = {'02adfedfghikg' : '1'}
    # if not _search_for_and_kick_player('02adfedfgh1kg', 'twat', teams):
    #     print('Failed to kick player')

    # input('enter')
    # quit()
        
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
        input("Press a key")
        print('Program terminated')