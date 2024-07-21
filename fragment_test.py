from engine import Engine
from fragments.grid import Grid
from fragments.settings import Settings

screen_dimension = Settings.SCREEN_SIZE.value, Settings.SCREEN_SIZE.value


def mainLoop():
    print("Starting Fragment Test")
    grid = Grid()
    engine = Engine(screen_dimension)

    def nestedLoop():
        print("Running Nested Loop")
        grid.drawNodes(engine.screen)

    engine.run(nestedLoop)
    


if __name__ == '__main__':
    mainLoop()