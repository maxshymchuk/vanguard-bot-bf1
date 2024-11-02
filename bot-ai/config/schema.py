schema = {
    '$schema': 'http://json-schema.org/draft-04/schema#',
    'type': 'object',
    'properties': {
        'server_name': {
            'type': 'string'
        },
        'window_title': {
            'type': 'string'
        },
        'screenshots_path': {
            'type': 'string'
        },
        'discord_webhook_url': {
            'type': 'string',
            'format': 'uri'
        },
        'player_name_similarity_probability': {
            'type': 'number',
            'minimum': 0,
            'maximum': 1
        },
        'weapon_text_similarity_probability': {
            'type': 'number',
            'minimum': 0,
            'maximum': 1
        },
        'icon_probability': {
            'type': 'number',
            'minimum': 0,
            'maximum': 1
        },
        'colors': {
            'type': 'object',
            'properties': {
                'ally_color': {
                    'type': 'string',
                    "pattern": r"^(\d+),(\d+),(\d+)$"
                },
                'enemy_color': {
                    'type': 'string',
                    "pattern": r"^(\d+),(\d+),(\d+)$"
                },
                'squad_color': {
                    'type': 'string',
                    "pattern": r"^(\d+),(\d+),(\d+)$"
                }
            },
            'additionalProperties': False
        },
        'recognition': {
            'type': 'object',
            'properties': {
                'spectator_text_box': {
                    'type': ['object', 'null'],
                    'properties': {
                        'x': {
                            'type': 'number',
                            'minimum': 0
                        },
                        'y': {
                            'type': 'number',
                            'minimum': 0
                        },
                        'width': {
                            'type': 'number',
                            'minimum': 0
                        },
                        'height': {
                            'type': 'number',
                            'minimum': 0
                        }
                    },
                    'required': ['x', 'y', 'width', 'height'],
                    'additionalProperties': False
                },
                'player_name_box': {
                    'type': ['object', 'null'],
                    'properties': {
                        'x': {
                            'type': 'number',
                            'minimum': 0
                        },
                        'y': {
                            'type': 'number',
                            'minimum': 0
                        },
                        'width': {
                            'type': 'number',
                            'minimum': 0
                        },
                        'height': {
                            'type': 'number',
                            'minimum': 0
                        }
                    },
                    'required': ['x', 'y', 'width', 'height'],
                    'additionalProperties': False
                },
                'weapon_icon_box': {
                    'type': ['object', 'null'],
                    'properties': {
                        'x': {
                            'type': 'number',
                            'minimum': 0
                        },
                        'y': {
                            'type': 'number',
                            'minimum': 0
                        },
                        'width': {
                            'type': 'number',
                            'minimum': 0
                        },
                        'height': {
                            'type': 'number',
                            'minimum': 0
                        }
                    },
                    'required': ['x', 'y', 'width', 'height'],
                    'additionalProperties': False
                },
                'weapon_name_box': {
                    'type': ['object', 'null'],
                    'properties': {
                        'x': {
                            'type': 'number',
                            'minimum': 0
                        },
                        'y': {
                            'type': 'number',
                            'minimum': 0
                        },
                        'width': {
                            'type': 'number',
                            'minimum': 0
                        },
                        'height': {
                            'type': 'number',
                            'minimum': 0
                        }
                    },
                    'required': ['x', 'y', 'width', 'height'],
                    'additionalProperties': False
                }
            },
            'additionalProperties': False
        },
        'banned_weapons': {
            'type': ['object', 'null'],
            'patternProperties': {
                '^': {
                    'type': 'array',
                    'items': [
                        {
                            'type': 'array',
                            'minItems': 1,
                            'items': {
                                'type': 'string'
                            }
                        },
                        {
                            'type': 'string'
                        }
                    ]
                }
            }
        }
    },
    'additionalProperties': False
}