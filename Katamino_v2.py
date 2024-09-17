from Blocks import Blocks

class main:
    def __init__(self):
        self.blocks = Blocks()
        self.board = []
        self.ghost_index = 0
        self.objects = {}
        self.activated = {}
        self.physical_board = []

        # testing
        self.set_board_size(3) # setup the board
        self.display_board()
        self.create_ghosts(self.blocks.Orange) # creates all the ghosts for a given object
        self.create_ghosts(self.blocks.Brown)
        self.create_ghosts(self.blocks.Green)
        self.display_board()
        self.place_block(0,0,self.blocks.Orange,0)
        self.display_board()
        self.place_block(0,1,self.blocks.Orange,0)
        self.display_board()
        self.place_block(1,1,self.blocks.Orange,0)
        self.display_board()
        # end testing
    
    def set_board_size(self, size):
        for row in range(5):
            self.board.append([])
            self.physical_board.append([])
            for _ in range(size):
                self.board[row].append([])
                self.physical_board[row].append("[ ]")
    
    def place_block(self, row, col, obj_block, angle):
        cells = obj_block[angle]
        fail = False
        shape = []
        for test in cells:
            roffset = row+test[0]
            coffset = col+test[1]
            try:
                tmp = self.board[roffset][coffset]
                shape.append((roffset,coffset))
                tmp2 = self.physical_board[roffset][coffset]
                if tmp2 == "[+]":
                    fail = True
                    shape = []
            except:
                fail = True
                shape = []
        if not fail:
            for cell in shape:
                r = cell[0]
                c = cell[1]
                test = self.board[r][c]
                for index in test:
                    self.activated[index] = False
                self.physical_board[r][c] = "[+]"
    
    def pick_up_block(self, row, col):
        pass

    def create_ghosts(self, obj_block):
        # go over the entire board
        r = 0
        c = 0
        for row in self.board:
            for cell in row:
                # test if the ghost can be placed in this cell
                for angle, locations in obj_block.items():
                    form = []
                    fail = False
                    for loc in locations:
                        roffset = r+loc[0]
                        coffset = c+loc[1]
                        try:
                            test = self.board[roffset][coffset]
                            form.append((roffset,coffset))
                        except:
                            form = []
                            fail = True
                    if not fail:
                        index = self.ghost_index
                        self.ghost_index += 1
                        for add in form:
                            self.board[add[0]][add[1]].append(index)
                            self.physical_board[add[0]][add[1]] = "[_]"
                            if not index in self.objects:
                                self.objects[index] = []
                            self.objects[index].append((add[0],add[1]))
                            self.activated[index] = True
                c += 1
            c = 0
            r += 1

    def display_board(self):
        display = ""
        for row in self.board:
            display += "|"
            for col in row:
                score = len(col)
                for index in col:
                    if not self.activated[index]:
                        score -= 1
                display += str(score).zfill(3)+"|"
            display += "\n"
        print(display)

        display = ""
        r = 0
        c = 0
        for row in self.physical_board:
            for col in row:
                score = len(self.board[r][c])
                for index in self.board[r][c]:
                    if not self.activated[index]:
                        score -= 1
                if score == 0 and self.physical_board[r][c] == "[_]":
                    self.physical_board[r][c] = "[ ]"
                display += self.physical_board[r][c]
                c += 1
            display += "\n"
            c = 0
            r += 1
        print(display)


        """
        for row in self.board:
            print(row)
        print("\nObjects:")
        for inx,cols in self.objects.items():
            print(inx,cols)
        print("\nActivated:")
        for inx,cols in self.activated.items():
            print(inx,cols)
        """

    def locnme(self,row,col):
        return str(row)+":"+str(col)
    
main()