from classes import CliArgs
from dataclasses import dataclass
from helpers import check_if_file
from .parser import parser

@dataclass
class CliResult:
    immediate_start = False
    verbose = False
    config_path: str | None = None

def init() -> CliResult:
    res = CliResult()
    args, unknown = parser.parse_known_args()
    if CliArgs.START in args:
        res.immediate_start = args.start
    if CliArgs.VERBOSE in args:
        res.verbose = args.verbose
    if CliArgs.CONFIG in args:
        try:
            if not check_if_file(args.config):
                raise
            res.config_path = args.config
        except:
            print('Config path is invalid, using default config')
    return res