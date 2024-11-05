from enum import StrEnum
from dataclasses import dataclass

@dataclass
class Box():
    x: int = None
    y: int = None
    width: int = None
    height: int = None

class CliArgs(StrEnum):
    START = 'start'
    VERBOSE = 'verbose'
    CONFIG = 'config'
    RESETUP = 'resetup'
    SCREENSHOT = 'screenshot'