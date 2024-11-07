from discord import SyncWebhook

config_path = 'config.json'
verbose = False
should_save_screenshot = False

window_title = 'Battlefield™ 1'
server_name = '![VG]Vanguard'
screenshots_path = 'screenshots'

pause_hotkey = 'ctrl+p'
rotate_delay = 0.0
minimum_player_count = 50

weapon_text_similarity_probability = 0.8
player_name_similarity_probability = 0.8
icon_probability = 0.8

discord_webhook_url = 'https://discord.com/api/webhooks/1018551113257074709/VASl0wpyhk1fkfjJNizXTejNcI-95SZ-d3NCSF092eiYeqxcR98sOnG7FP_RT6UrI7wn'
webhook = SyncWebhook.from_url(discord_webhook_url)

ally_color = (64, 118, 199)
enemy_color = (189, 54, 49)
squad_color = (74, 155, 44)

player_name_box = None # Box()
weapon_icon_box = None # Box()
weapon_name_box = None # Box()
weapon_name_slot2_box = None # Box()
gadget_slot_1_box = None # Box()
gadget_slot_2_box = None # Box()

# dict: category : {[in game names], pretty name}
banned_weapons = {
    'smg08': 
        [
            ['SMG08/18Factory', 'SMG08/18Optical'], 
            'SMG 08'
        ]
}

banned_gadgets = [
        [
            ['Rifle Grenade - FR', 'ifle Grenade - FRG', 'Rifle Grenade - HE'],
            'rifle grenade'
        ]
    ]

# dict: category : [ [variant primary weapon names], [variant secondary weapon names], pretty name) ]
banned_vehicles = {
    'heavybomber':
        [ 
            [
                [ 
                    ['5x HE Cluster Bomb', 'HE Cluster Bombs'], ['HE Auto-Cannon']
                ],
                [
                    ['5x 50 kg HE Bombs'], ['5x 250 kg Demolition Bombs']
                ],
                [
                    ['5x Incendiary Cluster Bomb', 'Incendiary Cluster Bombs'], ['5x Gas Bombs']
                ]
            ],
            'heavy bomber'
        ],
    'LMG':
        [ 
            [
                [ 
                    ['LMG'], ['Anti-Tank Cannon', 'Anti-Aircraft Gun']
                ],
            ],
            'artillery truck'
        ],
    'HMG':
        [
            [
                [
                    ['HMG'], ['Airbust Mortar']
                ]
            ],
            'artillery truck'
        ]
}