from models import predict_icon
import config
from modules.utils import get_string_similarity
from .find_and_kick_player import find_and_kick_player

def _check_weapon_str(weapon_text, category) -> tuple[bool, str]:

    banned_weapons_list, pretty_name = config.banned_weapons[category]

    for banned_weapon_text in banned_weapons_list:
        probability = get_string_similarity(weapon_text, banned_weapon_text)
        if probability >= config.weapon_text_similarity_probability:
            return True, pretty_name
        
    return False, ''

def check_player_weapons(player: str, weapon_icon_image, weapon_text: str) -> None:

    preds, probs = predict_icon(weapon_icon_image)
    prediction = preds[0]
    probability = probs[0]

    isBanned = False
    banned_weapon_name = ''

    print(f'Player {player} has weapon {weapon_text} in category {prediction} with probability {probability}')

    if probability >= config.icon_probability:
        if prediction != 'allowedprimaryguns':
            isBanned, banned_weapon_name = _check_weapon_str(weapon_text, prediction)
    else:
        print(f'Probability {str(probability)} too low, only checking weapon string')
        isBanned, banned_weapon_name = _check_weapon_str(weapon_text)

    if isBanned:
        find_and_kick_player(player, f'No {banned_weapon_name}, Read Rules')
