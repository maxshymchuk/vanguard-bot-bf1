from enum import StrEnum
from dataclasses import dataclass

@dataclass
class Coordinate():
    x: int = None
    y: int = None

@dataclass
class Box(Coordinate):
    width: int = None
    height: int = None

class CliArgs(StrEnum):
    # flags
    START = 'start'
    VERBOSE = 'verbose'
    CONFIG = 'config'
    SCREENSHOT = 'screenshot'