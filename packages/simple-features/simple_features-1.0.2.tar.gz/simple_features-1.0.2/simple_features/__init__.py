__version__ = '1.0.2'
import os, time

def clear():
  os.system('clear')

def wait(sec):
  time.sleep(sec)

# Regular colors (Foreground)
black = "\033[0;30m"
red = "\033[0;31m"
green = "\033[0;32m"
yellow = "\033[0;33m"
blue = "\033[0;34m"
magenta = "\033[0;35m"
cyan = "\033[0;36m"
white = "\033[0;37m"

# Bright colors (Foreground)
br_black = "\033[0;90m"
br_red = "\033[0;91m"
br_green = "\033[0;92m"
br_yellow = "\033[0;93m"
br_blue = "\033[0;94m"
br_magenta = "\033[0;95m"
br_cyan = "\033[0;96m"
br_white = "\033[0;97m"

# Regular colors (Background)
bg_black = "\033[0;40m"
bg_red = "\033[0;41m"
bg_green = "\033[0;42m"
bg_yellow = "\033[0;43m"
bg_blue = "\033[0;44m"
bg_magenta = "\033[0;45m"
bg_cyan = "\033[0;46m"
bg_white = "\033[0;47m"

# Bright colors (Background)
bg_br_black = "\033[0;100m"
bg_br_red = "\033[0;101m"
bg_br_green = "\033[0;102m"
bg_br_yellow = "\033[0;103m"
bg_br_blue = "\033[0;104m"
bg_br_magenta = "\033[0;105m"
bg_br_cyan = "\033[0;106m"
bg_br_white = "\033[0;107m"

reset = '\033[0m'