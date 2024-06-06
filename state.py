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
        if node.A > self.A:
            self.minusA()
        else:
            self.addA()
        
        if node.B > self.B:
            self.minusB()
        else:
            self.addB()