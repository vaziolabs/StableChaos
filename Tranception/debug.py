debug_level = 3

def debug(level, message):
    if level <= debug_level:
        print(message)