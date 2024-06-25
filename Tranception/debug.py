debug_level = 2

def debug(level, message):
    if level <= debug_level:
        print(message)