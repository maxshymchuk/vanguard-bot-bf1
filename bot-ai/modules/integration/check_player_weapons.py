from mss import mss
import config
from modules.screenshot import ScreenshotManager, crop_image_array
from modules.utils import get_string_similarity, string_is_similar_to
from .find_and_kick_player import find_and_kick_player
from modules.recognition import recognize_text
import warnings
# This is not ideal but ImageAI generates a few long warnings that we can't do much about so suppress them...
warnings.simplefilter('ignore', UserWarning)
warnings.simplefilter('ignore', FutureWarning)
from models import predict_icon
import traceback

# Checks all categories
def _check_weapon_str(game_img, screenshotmanager: ScreenshotManager, should_save_screenshot) -> tuple[bool, str]:
    weapon_image = crop_image_array(game_img, config.weapon_name_box)
    weapon_text = recognize_text(weapon_image)
    if weapon_text:
        print(f'weapon string is {weapon_text}')
        for banned_weapons_list, pretty_name in config.banned_weapons.values():
            for banned_weapon_text in banned_weapons_list:
                if string_is_similar_to(weapon_text, banned_weapon_text, config.weapon_text_similarity_probability):
                    if should_save_screenshot:
                        screenshotmanager.save_screenshots([(weapon_image, weapon_text)], [weapon_text])
                    return True, pretty_name
    return False, ''

# Checks a specific category
def _check_weapon_str_category(category, game_img, screenshotmanager, should_save_screenshot) -> tuple[bool, str]:
    weapon_image = crop_image_array(game_img, config.weapon_name_box)
    weapon_text = recognize_text(weapon_image)
    if weapon_text:
        print(f'weapon string is {weapon_text}')
        banned_weapons_list, pretty_name = config.banned_weapons[category]

        for banned_weapon_text in banned_weapons_list:
            if string_is_similar_to(weapon_text, banned_weapon_text, config.weapon_text_similarity_probability):
                if should_save_screenshot:
                    screenshotmanager.save_screenshots([(weapon_image, weapon_text)], [weapon_text])
                return True, pretty_name
        
    return False, ''

def _check_gadgets_str(game_img, screenshotmanager: ScreenshotManager, should_save_screenshot) -> tuple[bool, str]:
    gadget_slot1_image = crop_image_array(game_img, config.gadget_slot_1_box)
    gadget_slot2_image = crop_image_array(game_img, config.gadget_slot_2_box)
    gadget_slot1_text = recognize_text(gadget_slot1_image)
    gadget_slot2_text = recognize_text(gadget_slot2_image)

    if not gadget_slot1_text:
        gadget_slot1_text = ''
    if not gadget_slot2_text:
        gadget_slot2_text = ''

    for banned_gadget_list, pretty_name in config.banned_gadgets:
        for banned_gadget in banned_gadget_list:
            if string_is_similar_to(gadget_slot1_text, banned_gadget, config.weapon_text_similarity_probability):
                if should_save_screenshot:
                    screenshotmanager.save_screenshots([(gadget_slot1_image, 'gadget1'), (gadget_slot2_image, 'gadget2')], [gadget_slot1_text, gadget_slot2_text])
                return True, pretty_name
            if string_is_similar_to(gadget_slot2_text, banned_gadget, config.weapon_text_similarity_probability):
                if should_save_screenshot:
                    screenshotmanager.save_screenshots([(gadget_slot1_image, 'gadget1'), (gadget_slot2_image, 'gadget2')], [gadget_slot1_text, gadget_slot2_text])
                return True, pretty_name
    return False, ''

# Check the names of the weapons in slot 1 and slot 2 and returns True if one of them matches
def _check_vehicle_slot1_or_slot2(category: str, game_img, screenshotmanager, should_save_screenshot) -> tuple[bool, str]:
    weapon_slot1_image = crop_image_array(game_img, config.weapon_name_box)
    weapon_slot2_image = crop_image_array(game_img, config.weapon_name_slot2_box)

    weapon_slot1_text = recognize_text(weapon_slot1_image)
    weapon_slot2_text = recognize_text(weapon_slot2_image)

    variants_list, pretty_name = config.banned_vehicles[category]
    for primary_names, secondary_names in variants_list:
        for primary in primary_names:
            if string_is_similar_to(weapon_slot1_text, primary, config.weapon_text_similarity_probability):
                if should_save_screenshot:
                    screenshotmanager.save_screenshots([(weapon_slot1_image, 'slot1')], [weapon_slot1_text])
                return True, pretty_name
        for secondary in secondary_names:
            if string_is_similar_to(weapon_slot2_text, secondary, config.weapon_text_similarity_probability):
                if should_save_screenshot:
                    screenshotmanager.save_screenshots([(weapon_slot2_image, 'slot2')], [weapon_slot2_text])  
                return True, pretty_name
    return False, ''

def _check_vehicle_slot2(category: str, game_img, screenshotmanager, should_save_screenshot):
    weapon_slot2_image = crop_image_array(game_img, config.weapon_name_slot2_box)
    weapon_slot2_text = recognize_text(weapon_slot2_image)

    if weapon_slot2_text:
        #print(f'weapon slot 2 text for arty truck is {weapon_slot2_text}')
        variants_list, pretty_name = config.banned_vehicles[category]
        for _, secondary_names in variants_list:
            for secondary in secondary_names:
                if string_is_similar_to(weapon_slot2_text, secondary, config.weapon_text_similarity_probability):
                    if should_save_screenshot:
                        screenshotmanager.save_screenshots([(weapon_slot2_image, 'slot2')], [category, weapon_slot2_text])
                    return True, pretty_name
    else:
        print('weapon_slot_2 failed')
    return False, ''

def check_player_weapons(player: str, game_img, should_save_screenshot: bool) -> None:
    try:
        screenshotmanager = ScreenshotManager(player)

        weapon_icon_image = crop_image_array(game_img, config.weapon_icon_box)
        preds, probs = predict_icon(weapon_icon_image)
        prediction = preds[0]
        probability = probs[0] / 100

        isBanned = False
        banned_weapon_name = ''

        if probability >= config.icon_probability:
            print(f'Probability {probability} for prediction {prediction} is enough')
            match prediction:
                case 'smg08':
                    isBanned, banned_weapon_name = _check_weapon_str_category(prediction, game_img, screenshotmanager, should_save_screenshot)
                case 'heavybomber':
                    isBanned, banned_weapon_name = _check_vehicle_slot1_or_slot2(prediction, game_img, screenshotmanager, should_save_screenshot)
                case 'lmg' | 'hmg':
                    isBanned, banned_weapon_name = _check_vehicle_slot2(prediction, game_img, screenshotmanager, should_save_screenshot)
                case 'allowedprimaryguns':
                    isBanned, banned_weapon_name = _check_gadgets_str(game_img, screenshotmanager, should_save_screenshot)
            # TODO: save weapon icon here
        else:
            print(f'Probability {probability} in category {prediction} too low, checking weapon string only')
            isBanned, banned_weapon_name = _check_weapon_str(game_img, screenshotmanager, should_save_screenshot)

        if isBanned:
            print(f'Player {player} kicked for No {banned_weapon_name}')
            find_and_kick_player(player, f'No {banned_weapon_name}, Read Rules')
    except Exception as e:
        print('Thread exception ' + str(e))
        print(traceback.format_exc())
