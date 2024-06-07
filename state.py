# Possible States are A+1 to A-1 and B+1 to B-1

class State:
    def __init__(self, A, B):
        self.A = A
        self.B = B

    def addA(self):
        self.A += 1 if self.A < 1 else 1
    
    def addB(self):
        self.B += 1 if self.B < 1 else 1
    
    def minusA(self):
        self.A -= 1 if self.A > -1 else -1

    def minusB(self):
        self.B -= 1 if self.B > -1 else -1
    
    def repel(self, node):
        if node.A == 1 and node.B == 1:
            self.A = -1
            self.B = -1
        elif node.A == -1 and node.B == -1:
            self.A = 1
            self.B = 1

        if node.A > 0:
            self.minusA()
        elif node.A < 0:
            self.addA()
        
        if node.B < 0:
            self.minusB()
        elif node.B > 0:
            self.addB()