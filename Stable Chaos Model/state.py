# Possible States are A+1 to A-1 and B+1 to B-1

class State:
    def __init__(self, A, B):
        self.A = A
        self.B = B

    def addA(self):
        temp_A = self.A + .0987
        self.A = temp_A if temp_A < 1.0 else 1.0
    
    def addB(self):
        temp_B = self.B + .0987
        self.B = temp_B if temp_B < 1.0 else 1.0

    def minusA(self):
        temp_A = self.A - .0987
        self.A = temp_A if temp_A > -1.0 else -1.0

    def minusB(self):
        temp_B = self.B - .0987
        self.B = temp_B if temp_B > -1.0 else -1.0
    
    def repel(self, node):
        if node.A > self.A:
            self.minusA()
        elif node.A < self.A:
            self.addA()
        
        if node.B < self.B:
            self.minusB()
        elif node.B > self.B:
            self.addB()