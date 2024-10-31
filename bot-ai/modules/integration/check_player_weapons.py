from models import predict_icon
import config
from modules.utils import get_string_similarity

def _check_weapon_str(weapon_text) -> tuple[bool, str]:
    for banned_weapon_text in config.banned_weapons.keys():
        probability = get_string_similarity(weapon_text, banned_weapon_text)
        if probability >= config.weapon_text_similarity_probability:
            return True, config.banned_weapons[banned_weapon_text]
        
    return False, ''

# Return: Whether the player is using a banned weapon, the weapon text, predicted weapon category, probability of predicted weapon category
def check_player_weapons(weapon_icon_image, weapon_text: str) -> tuple[bool, str, str, float]:
    if weapon_icon_image:
        try:
            preds, probs = predict_icon(weapon_icon_image)
            prediction = preds[0]
            probability = probs[0]
            if prediction != 'allowedprimaryguns' and probability >= config.icon_probability:
                return _check_weapon_str(weapon_text), prediction, probability
            else:
                return False, weapon_text, prediction, probability
        except Exception as e:
            print(e)
            return False, weapon_text, '', 0
    elif weapon_text:
        return _check_weapon_str(weapon_text), '', 0
    
    # weapon_icon_image and weapon_text were both None, this should never happen
    return False, weapon_text, '', 0
