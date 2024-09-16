from Blocks import Blocks
class block:
    def __init__(self, size):
        self.size = size

class main:
    def __init__(self):
        self.blocks = Blocks()
        self.board = []
        self.playing_blocks = []

        ################  for testing  ################
        self.set_board_size(3)
        self.display_board()
        self.add_object_to_game(self.blocks.Orange)
        self.add_object_to_game(self.blocks.Brown)
        self.add_object_to_game(self.blocks.Green)
        self.display_board()
        self.place_block(0,0,self.playing_blocks[0],3)
        ###############################################
    
    def set_board_size(self, size):
        for row in range(5):
            self.board.append([])
            for _ in range(size):
                self.board[row].append(0)

    def add_object_to_game(self, obj_block):
        self.playing_blocks.append(obj_block)
        y = 0
        x = 0
        for row in self.board:
            for _ in row:
                self.create_ghost(y,x,obj_block)
                x += 1
            x = 0
            y += 1

    def create_ghost(self, y, x, obj_block):
        for cells in obj_block.values():
            shape = []
            fail = False        
            for cell in cells:
                xoffset = cell[1]
                yoffset = cell[0]
                try:
                    test = self.board[y+yoffset][x+xoffset]
                    shape.append((y+yoffset,x+xoffset))
                except:
                    shape = []
                    fail = True
            if not fail:
                for add in shape:
                    self.board[add[0]][add[1]] += 1

    def place_block(self, y, x, obj_block, angle):
        self.board = 
    
    def display_board(self):
        display = ""
        for row in self.board:
            display += "|"
            for col in row:
                display += str(col).zfill(3)+"|"
            display += "\n"
        print(display)

main()