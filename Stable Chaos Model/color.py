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
    def lerp(color_A, color_B, t):
        t = (t + 1.0) / 2.0 # This value is originally -1 to 1

        color_A = color_A.value if isinstance(color_A, Color) else color_A
        color_B = color_B.value if isinstance(color_B, Color) else color_B

        r = int(color_A[0] + (color_B[0] - color_A[0]) * t)
        g = int(color_A[1] + (color_B[1] - color_A[1]) * t)
        b = int(color_A[2] + (color_B[2] - color_A[2]) * t)
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
        A_Color = Color.lerp(Color.WHITE_FILL, Color.BLUE, state.A)
        B_Color = Color.lerp(Color.BLACK_FILL, Color.RED, state.B)
        return Color.lerp(A_Color, B_Color, (state.A + state.B) / 2.0)
