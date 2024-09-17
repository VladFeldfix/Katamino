from Blocks import Blocks

Ghost = "Ghost"
Solid = "Solid"
Dead = "Daed"

class Obj_Block:
    def __init__(self, color, ghosts):
        self.color = color # Blue, Orange, Grey string
        self.ghosts = ghosts # [ghost1, ghost2, ghost3] a list of ghost objects
        self.selected_ghost = 0 # the index of the solid ghost int

class Obj_Ghost:
    def __init__(self, name, cells):
        self.name = name # ghost1, ghost2, ghost3 string
        self.cells = cells # [(0,0),(1,0),(2,0),(3,0),(4,0)] a list of locations on the board
        self.state = Ghost # Ghost, Solid, Dead string

class main:
    def __init__(self):
        self.blocks = Blocks() # load the shapes of all the blocks
        self.objects = [] # a list of block objects
        self.board = [] # 2d list where each col is list of ghost names that are located there
        self.names = [] # a list of object names
        self.ghost_name_index = 0

        #### TEST ####
        self.setup_board(3)
        self.create_object(self.blocks.Orange)
        #self.create_object(self.blocks.Brown)
        #self.create_object(self.blocks.Green)
        self.display_board()
        ##############

    def calculate(self):
        # the calculation method:
        # START LOOP
        # go to next object in self.objects (start from 0)
        # set the objects' selected_ghost proparty to the next index (start from 0)
        # go to the next object in the list self.objects
        # select the first available ghost and set selected_ghost to the index of the ghost
        # if there are no available shosts at go back to the prev self.objects index and goto START LOOP
        pass
    
    def create_object(self, obj_block):
        r = 0
        c = 0
        name = ""
        for row in self.board:
            for col in row:
                for angle, cells in obj_block.items(): # self.Orange[0] = ((0,0),(0,1),(1,0),(2,0),(3,0))
                    if angle != "Name":
                        fail = False
                        shape = []
                        for cell in cells:
                            roffset = r + cell[0]
                            coffset = c + cell[1]
                            try:
                                test = self.board[roffset][coffset]
                                shape.append((roffset,coffset))
                            except:
                                fail = True
                                shape = []
                        if not fail:
                            self.ghost_name_index += 1
                            ghost_name = "Ghost"+str(self.ghost_name_index)
                            if not name in self.names:
                                self.names.append(name)
                                obj = Obj_Block(name, [])
                                self.objects.append(obj)
                            ghost = Obj_Ghost(ghost_name, [])
                            for add in shape:
                                self.board[add[0]][add[1]] = ghost_name
                                ghost.cells.append((add[0],add[1]))
                            obj.ghosts.append(ghost)
                    else:
                        name = angle
                c += 1
            c = 0
            r += 1

    def setup_board(self, size):
        for row in range(5):
            self.board.append([])
            for _ in range(size):
                self.board[row].append([])
    
    def display_board(self):
        display = ""
        for row in self.board:
            display += "|"
            for col in row:
                display += str(col)+","
            display += "|\n"
        print(display)

main()