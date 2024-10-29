from discord import SyncWebhook
from pathlib import Path
from classes import Box, Coordinate

window_title = 'Battlefield™ 1'
screenshots_path = Path.cwd() / 'screenshots'
config_path = Path.cwd() / 'config' / 'config.txt'

ally_color = (64, 118, 199)
enemy_color = (189, 54, 49)
squad_color = (74, 155, 44)

weapon_text_similarity_probability = 0.7
player_name_similarity_probability = 0.3

webhook = SyncWebhook.from_url('https://discord.com/api/webhooks/1018551113257074709/VASl0wpyhk1fkfjJNizXTejNcI-95SZ-d3NCSF092eiYeqxcR98sOnG7FP_RT6UrI7wn')

# dict: common recognition name : pretty name for kick messages
banned_weapons = {
    'SMG08I8Factory' : 'SMG08'
}
#'5x HE Cluster Bomb' : 'Heavy Bomber', 'HE Cluster Bombs' : 'Heavy Bomber'}

# controllable by cli arguments
should_read_config = False
verbose_errors = False

next_player_button = Coordinate()
player_name = Box()
weapon_name = Box()