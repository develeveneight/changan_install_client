from datetime import datetime


class Cl:
    black = '\u001b[30m'
    red = '\u001b[31m'
    green = '\u001b[32m'
    yellow = '\u001b[33m'
    blue = '\u001b[34m'
    purple = '\u001b[35m'
    magenta = '\u001b[36m'
    white = '\u001b[37m'
    reset = '\u001b[0m'


def log(msg, debug=False):
    if debug is False:
        print(f"{Cl.magenta}({datetime.now().strftime('%m.%d.%Y, %H:%M')}){Cl.reset} {msg}{Cl.reset}")
    if debug is True:
        print(f"{Cl.red}({datetime.now().strftime('%m.%d.%Y, %H:%M')}){Cl.reset} {msg}{Cl.reset}")
