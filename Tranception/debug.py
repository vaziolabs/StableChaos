debug_level = 4

def debug(level, message):
    if level <= debug_level:
        print(message)