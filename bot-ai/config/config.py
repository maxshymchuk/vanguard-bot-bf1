from discord import SyncWebhook

config_path = 'config.json'
verbose_errors = False
should_save_screenshot = False

window_title = 'Battlefield™ 1'
server_name = '![VG]Vanguard'
screenshots_path = 'screenshots'

weapon_text_similarity_probability = 0.8
player_name_similarity_probability = 0.8
icon_probability = 0.8

discord_webhook_url = 'https://discord.com/api/webhooks/1018551113257074709/VASl0wpyhk1fkfjJNizXTejNcI-95SZ-d3NCSF092eiYeqxcR98sOnG7FP_RT6UrI7wn'
webhook = SyncWebhook.from_url(discord_webhook_url)

ally_color = (64, 118, 199)
enemy_color = (189, 54, 49)
squad_color = (74, 155, 44)

change_player_button_coordinate = None # Coordinate()
player_view_button_coordinate = None # Coordinate()
third_person_view_button_coordinate = None # Coordinate()
spectator_text_box = None # Box()
player_name_box = None # Box()
weapon_icon_box = None # Box()
weapon_name_box = None # Box()

# dict: category : {[in game names], pretty name}
banned_weapons = {
    'smg08': 
        [
            ['SMG08/18Factory', 'SMG08/18Optical'], 
            'SMG 08'
        ], 
    'heavybomber': 
        [
            ['5x HE Cluster Bomb', 'HE Cluster Bombs', '5x 50 kg HE Bomb', '5x Incendiary Cluster Bomb', 'Incendiary Cluster Bomb'], 
            'heavy bomber'
        ]
}