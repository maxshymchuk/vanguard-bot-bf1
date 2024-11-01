import argparse
from classes import CliArgs

parser = argparse.ArgumentParser(
    prog = 'Vanguard Bot Tool',
    exit_on_error = False,
    argument_default = argparse.SUPPRESS
)

parser.add_argument('-s', f'--{CliArgs.START}', action='store_true')
parser.add_argument('-v', f'--{CliArgs.VERBOSE}', action='store_true')
parser.add_argument('-sc', f'--{CliArgs.SCREENSHOT}', action='store_true')
parser.add_argument('-r', f'--{CliArgs.RESETUP}', action='store_true')
parser.add_argument('-c', f'--{CliArgs.CONFIG}', help = 'path to config file')