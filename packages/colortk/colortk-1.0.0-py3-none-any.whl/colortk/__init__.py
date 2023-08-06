from typing import Union,Optional
import random as __random

COLORS = {
    "red": 31,
    "green": 32,
    "yellow": 33,
    "blue": 34,
    "magenta": 35,
    "cyan": 36,
}

def __random_color_code():
    return __random.randint(31,36)

def __color_code(color:Optional[Union[str,int]]=None):
    if isinstance(color,int):
        color = color
    elif isinstance(color,str):
        color = COLORS.get(color,None)
        if color is None:
            color = __random_color_code()
    else:
        color = __random_color_code()
    return color
    
__colorize = lambda __string,__color_code:f"\033[1;{__color_code}m{__string}\033[0m"

def colorizer(color:Optional[Union[str,int]]=None):
    color_code = __color_code(color=color)
    def colorize(__string:str) -> str:
        return __colorize(__string,color_code)
    return colorize


