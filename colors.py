#!/usr/bin/env python3

import colorama
from colorama import Fore



# Custom color declarations
#LIGHT_GRAY = "\033[0;37m"
DARK_GRAY = "\033[1;30m"
LIGHT_BLUE = "\033[1;34m"
ORANGE = "\033[38;2;255;165;0m"

# Styles
ITALIC = "\033[3m"

# Color aliases
GRAY = DARK_GRAY
RED, GREEN = Fore.RED, Fore.GREEN
BLUE = LIGHT_BLUE


# Colorama init. A rather barebones library, but it does enough.
colorama.init(autoreset=True)
