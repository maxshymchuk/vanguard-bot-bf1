from classes import CliArgs
from dataclasses import dataclass
from .parser import parser

@dataclass
class CliResult:
    immediate_start = False
    verbose = False
    setup_config = False
    screenshot = False

def init() -> CliResult:
    res = CliResult()
    args, unknown = parser.parse_known_args()
    if CliArgs.START in args:
        res.immediate_start = args.start
    if CliArgs.VERBOSE in args:
        res.verbose = args.verbose
    if CliArgs.CONFIG in args:
        res.setupconfig = args.config
    if CliArgs.SCREENSHOT in args:
        res.screenshot = args.screenshot
    return res