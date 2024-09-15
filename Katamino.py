class block:
    def __init__(self, size):
        self.size = size

class main:
    def __init__(self):
        self.obj_red = block(((0,1),(1,0),(1,1),(1,2),(2,1))) # (row, col)
        #self.obj_ = block(((),(),(),(),()))

        self.board = []

        ################  for testing  ################
        self.set_board_size(5)
        self.display_board()
        self.add_object_to_game(self.obj_red)
        self.display_board()
        ###############################################
    
    def set_board_size(self, size):
        for row in range(5):
            self.board.append([])
            for col in range(size):
                self.board[row].append(0)

    def add_object_to_game(self, obj_block):
        y = 0
        x = 0
        for row in self.board:
            for col in row:
                self.create_ghost(y,x,obj_block)
                x += 1
            x = 0
            y += 1

    def create_ghost(self, x, y, obj_block):
        shape = []
        fail = False
        for cell in obj_block.size:
            xoffset = cell[0]
            yoffset = cell[1]
            try:
                test = self.board[x+xoffset][y+yoffset]
                shape.append((x+xoffset,y+yoffset))
            except:
                shape = []
                fail = True
        if not fail:
            for add in shape:
                self.board[add[0]][add[1]] += 1

    def place_block(self, x, y, obj_block):
        pass
    
    def display_board(self):
        display = ""
        for row in self.board:
            display += "|"
            for col in row:
                display += str(col)+"|"
            display += "\n"
        print(display)

main()