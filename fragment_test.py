from engine import Engine
from fragments.grid import Grid
from fragments.settings import Settings

screen_dimension = Settings.SCREEN_SIZE.value, Settings.SCREEN_SIZE.value

def mainLoop():
    fn = (lambda: None)
    Engine(screen_dimension, Grid()).run(fn)


if __name__ == '__main__':
    mainLoop()