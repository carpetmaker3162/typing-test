import os

def _unix_getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def _win_getch():
    return msvcrt.getch()

if os.name == "nt":
    import msvcrt
    getch = _win_getch
else:
    import sys, tty, termios
    getch = _unix_getch