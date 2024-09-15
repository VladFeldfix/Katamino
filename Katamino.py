class block:
    def __init__(self, size):
        self.size = size

class main:
    def __init__(self):
        self.obj_red = block(((0,1),(1,0),(1,1),(1,2),(2,1))) # (row, col)
        self.obj_ = block(((),(),(),(),()))
    
main()