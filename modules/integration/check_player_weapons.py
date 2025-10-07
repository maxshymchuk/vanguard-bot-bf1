from dataclasses import dataclass
from classes import Box
from typing import List
import config
from modules.screenshot import ScreenshotManager, crop_image_array
from modules.utils import string_is_similar_to, available_weapon_symbols, available_nickname_symbols
from .find_and_kick_player import find_and_kick_player
from modules.recognition import recognize_text
from modules.image_enhancer import enhance_weapon_image
import traceback
from models import Classifier
import globals

class Slot:
    def __init__(self, slot_num: int, game_img, box: Box):
        self.slot_num = slot_num
        self.image = enhance_weapon_image(crop_image_array(game_img, box))
        self.text = recognize_text(self.image, available_weapon_symbols)

@dataclass
class VehicleVariant:
    primary_names: List[str]
    secondary_names: List[str]

    def __getitem__(self, slot: Slot):
        if slot.slot_num == 1:
            return self.primary_names
        elif slot.slot_num == 2:
            return self.secondary_names
        else:
            raise IndexError('Slot index out of range')

def _check_slot(category, slot: Slot):
    if slot.text:
        banned_names, pretty_name = config.banned_weapons[category]
        for banned_name in banned_names:
            if string_is_similar_to(slot.text, banned_name, config.weapon_text_similarity_probability):
                return True, pretty_name
    return False, ''
            
def _find_vehicle_variant_by_slot(vehicletype, slot: Slot):
    variants, pretty_name = config.banned_vehicles[vehicletype]
    if slot.text:
        for variant in variants:
            variant = VehicleVariant(variant[0], variant[1])
            for banned_name in variant[slot]:
                if string_is_similar_to(slot.text, banned_name, config.gadget_text_similarity_probability):
                    return True, pretty_name, variant
    return False, pretty_name, None

def _check_slot_by_vehicle_variant(variant: VehicleVariant, slot: Slot):
    if slot.text:
        for banned_name in variant[slot]:
            if string_is_similar_to(slot.text, banned_name, config.gadget_text_similarity_probability):
                return True
    return False

def _check_gadgets_slots(slot3: Slot, slot4: Slot) -> tuple[bool, str]:
    
    if not slot3.text:
        slot3.text = ''
    if not slot4.text:
        slot4.text = ''

    for banned_gadget_list, pretty_name in config.banned_gadgets:
        for banned_gadget in banned_gadget_list:
            if string_is_similar_to(slot3.text, banned_gadget, config.gadget_text_similarity_probability) or string_is_similar_to(slot4.text, banned_gadget, config.gadget_text_similarity_probability):
                    return True, pretty_name
    return False, ''

def check_player_weapons(lock, classifier: Classifier, active_window, should_save_screenshot: bool) -> None:
    # try:
        screenshotmanager = ScreenshotManager()

        game_img = screenshotmanager.capture(active_window.top, active_window.left, active_window.width, active_window.height)

        player_name_img = crop_image_array(game_img, config.player_name_box)
        player = recognize_text(player_name_img, available_nickname_symbols)

        with lock:
            if not player or len(player) < 3: # Max player name length is 3 so if we read less than 3, the round might have ended
                if not globals.round_ended:
                    globals.no_player_count += 1
                    if globals.no_player_count == 2:
                        globals.round_ended = True
                        globals.no_player_count = 0
                return
            elif globals.round_ended:
                globals.round_ended = False
                globals.no_player_count = 0

            with globals.kick_lock:
                if player in globals.kick_list:
                    print(f'Player {player} already marked for kicking, skipping')
                    return
            
            if player == globals.last_player:
                globals.same_player_count += 1
                if globals.same_player_count == 2:
                    globals.same_player_count = 0
                    # Go other way
                    if globals.rotate_key == 'e':
                        globals.rotate_key = 'q'
                    else:
                        globals.rotate_key == 'e'
                    print(f'Got stuck, rotating other way using key {globals.rotate_key}')

        weapon_icon_image = crop_image_array(game_img, config.weapon_icon_box)
        prediction, probability = classifier.predict_icon(weapon_icon_image)

        isBanned = False
        banned_weapon_name = ''

        slot1 = Slot(1, game_img, config.weapon_name_box)
        slot2 = None
        slot3 = None
        slot4 = None

        #print(f'Player {player} has weapon {slot1.text} in category {prediction} with probability {probability}')

        # if should_save_screenshot:
        #     screenshotmanager.save_screenshots([(slot1.image, slot1.text)], [slot1.text])

        if probability >= config.icon_probability:
            #print(f'Probability {probability} for prediction {prediction} is enough')
            match prediction:
                case 'smg08':
                    isBanned, banned_weapon_name = _check_slot(prediction, slot1)
                case 'heavybomber': # Confirm via slot 1 text OR slot 2 text
                    slot2 = Slot(2, game_img, config.weapon_name_slot2_box)
                    isBanned, banned_weapon_name, variant = _find_vehicle_variant_by_slot(prediction, slot1)
                    if not isBanned:
                        isBanned, _, _ = _find_vehicle_variant_by_slot(prediction, slot2)
                case 'lmg' | 'hmg': # Confirm via slot 2 text
                    slot2 = Slot(2, game_img, config.weapon_name_slot2_box)
                    isBanned, banned_weapon_name, _ = _find_vehicle_variant_by_slot(prediction, slot2)
                case 'allowedprimaryguns':
                    slot3 = Slot(3, game_img, config.gadget_slot_1_box)
                    slot4 = Slot(4, game_img, config.gadget_slot_2_box)
                    isBanned, banned_weapon_name = _check_gadgets_slots(slot3, slot4)
        else:
            #print(f'Probability {probability} in category {prediction} too low, checking weapon string only')
            # Get weapon image 1
            for category in config.banned_weapons.keys(): # Check slot1 for normal weapons
                isBanned, banned_weapon_name = _check_slot(category, slot1)

            if not isBanned:
                # If not, check vehicle slot 1
                for vehicle_category in config.banned_vehicles.keys():
                    slot1Found, banned_weapon_name, variant = _find_vehicle_variant_by_slot(vehicle_category, slot1)
                    if slot1Found: # If yes, check slot 2 as well for confirmation
                        slot2 = Slot(2, game_img, config.weapon_name_slot2_box)
                        isBanned = _check_slot_by_vehicle_variant(variant, slot2)
                        if isBanned:
                            break

        if isBanned:
            if should_save_screenshot:
                screenshotmanager.new_folder(player)
            
                if slot3:
                    screenshotmanager.save_screenshots([(player_name_img, player), (slot3.image, 'gadget1'), (slot4.image, 'gadget2')], [player, slot3.text, slot3.text])
                elif slot2:
                    screenshotmanager.save_screenshots([(player_name_img, player), (weapon_icon_image, 'icon'), (slot1.image, slot1.text), (slot2.image, slot2.text)], [player, slot1.text, slot2.text])
                else:
                    screenshotmanager.save_screenshots([(player_name_img, player), (weapon_icon_image, 'icon'), (slot1.image, slot1.text)], [player, slot1.text])
                    
            #print(f'Player {player} kicked for No {banned_weapon_name}')
            find_and_kick_player(player, f'No {banned_weapon_name}, Read Rules')
    # except Exception as e:
    #     #print('Thread exception ' + str(e))
    # #    #print(traceback.format_exc())
