from Blocks import Blocks

class main:
    def __init__(self):
        self.blocks = Blocks()
        self.board = []
        self.playing_blocks = []
        self.ghosts = {}
        self.ghosts_status = {}
        self.contact_points = {}
        self.ghost_index = 0

        ################  for testing  ################
        self.set_board_size(3)
        self.display_board()
        self.add_object_to_game(self.blocks.Orange)
        #self.add_object_to_game(self.blocks.Brown)
        #self.add_object_to_game(self.blocks.Green)
        self.display_board()
        self.place_block(0,0,self.playing_blocks[0],3)
        self.display_board()
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
        index = self.ghost_index
        self.ghost_index += 1
        for key, cells in obj_block.items():
            if key != "Name":
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
                        yy = add[0]
                        xx = add[1]
                        self.board[yy][xx] += 1
                        if not index in self.ghosts:
                            self.ghosts[index] = []
                        self.ghosts[index].append((yy,xx))
                        self.ghosts_status[index] = True
                        loc = str(yy)+":"+str(xx)
                        if not loc in self.contact_points:
                            self.contact_points[loc] = []
                        self.contact_points[loc].append(index)

    def place_block(self, y, x, obj_block, angle):
        for cell in obj_block[angle]:
            yoffset = y+cell[0]
            xoffset = x+cell[1]
            self.delete_ghost(yoffset, xoffset)

    def delete_ghost(self, y, x):
        loc = str(y)+":"+str(x)
        ghosts = self.contact_points[loc]

        for index in ghosts:
            if self.ghosts_status[index]:
                for cell in self.ghosts[index]:
                    y = cell[0]
                    x = cell[1]
                    if self.board[y][x] > 0:
                        self.board[y][x] -= 1
                self.ghosts_status[index] = False
    
    def display_board(self):
        display = ""
        for row in self.board:
            display += "|"
            for col in row:
                display += str(col).zfill(3)+"|"
            display += "\n"
        print("BOAD:")
        print(display)
        print("ghosts:")
        print(self.ghosts)
        print("\ncontact_points:")
        print(self.contact_points)
        print("\nghosts_status:")
        print(self.ghosts_status)

main()