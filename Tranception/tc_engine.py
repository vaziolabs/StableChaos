import asyncio
import sys
from tranception import Tranception
sys.path.append('../')
from engine import Engine, Color

class TCEngine(Engine):
    def __init__(self, screen_size):
        super().__init__(screen_size, [])
        self.evokation = Tranception(100)

    def activate(self):
        asyncio.run(self.evokation.induce())