from enum import Enum

class Color(Enum):
    BLACK_OUTLINE = (33, 33, 33)
    WHITE_BACKGROUND = (222, 222, 222)
    BLACK_FILL = (0, 0, 0)
    WHITE_FILL = (255, 255, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    PURPLE = (128, 0, 128)

    def val(self):
        return self.value if isinstance(self.value, tuple) else self

    @staticmethod
    def lerp(self, other, t):
        value = other.val() if isinstance(other, Color) else other
        r = self.value[0] + (value[0] - self.value[0]) * t
        g = self.value[1] + (value[1] - self.value[1]) * t
        b = self.value[2] + (value[2] - self.value[2]) * t
        return (r, g, b)
    
    @staticmethod
    def fromPosition(i):
        if i == 0:
            return Color.RED
        elif i == 1:
            return Color.GREEN
        elif i == 2:
            return Color.BLUE
        else:
            return Color.WHITE_FILL
        
    @staticmethod
    def fromState(state):
        if state.A > 0 and state.B > 0:
            return Color.WHITE_FILL
        elif state.A < 0 and state.B < 0:
            return Color.BLACK_FILL
        elif state.A > 0 and state.B < 0:
            return Color.RED
        elif state.A < 0 and state.B > 0:
            return Color.BLUE
        else:
            return Color.PURPLE