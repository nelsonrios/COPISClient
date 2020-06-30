from enum import Enum

class Axis(Enum):
    X = "x"
    Y = "y"
    Z = "z"
    B = "b"
    C = "c"
    Plus = "++"
    Minus = "-"

class Tool_Ids(Enum):
    Play = 1
    Pause = 2
    Stop = 3
    Settings = 4

class Focus(Enum):
    Near1 = 1
    Near2 = 2
    Near3 = 3
    Far1 = 4
    Far2 = 5
    Far3 = 6