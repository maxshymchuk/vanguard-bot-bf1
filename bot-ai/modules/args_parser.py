import globals
import config

def check_rgb_str(str: str) -> tuple[int, int, int]:
    split = list(map(int, str.split(',')))
    return tuple(split) if len(split) == 3 else None

def init() -> bool:
    immediate_start = False
    try:
        args, unknown = globals.parser.parse_known_args()

        if 'start' in args:
            immediate_start = args.start

        if 'config' in args:
            config.should_read_config = args.config

        if 'verbose' in args:
            config.verbose_errors = args.verbose

        if 'ally_color' in args:
            print('ally_color')
            ally_color = check_rgb_str(args.ally_color)
            if ally_color:
                config.ally_color = ally_color

        if 'enemy_color' in args:
            enemy_color = check_rgb_str(args.enemy_color)
            if enemy_color:
                config.enemy_color = enemy_color

        if 'squad_color' in args and squad_color:
            squad_color = check_rgb_str(args.squad_color)
            if squad_color:
                config.squad_color = squad_color

    except:
        pass

    return immediate_start