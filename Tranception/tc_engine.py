import asyncio
import sys
from tranception import Tranception
sys.path.append('../')
from engine import Engine, Color

class TCEngine(Engine):
    def __init__(self, screen_size):
        super().__init__(screen_size, [])
        self.evokation = Tranception(100)

    # asyncio.create_task(node_list[0].rcv(440))
    # asyncio.create_task(node_list[0].snd(node_list[1]))