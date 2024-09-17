from Blocks import Blocks

Ghost = "Ghost"
Solid = "Solid"
Dead = "Daed"

class Obj_Block:
    def __init__(self):
        self.color = "" # Blue, Orange, Grey string
        self.ghosts = [] # [ghost1, ghost2, ghost3] a list of ghost objects
        self.selected_ghost = 0 # the index of the solid ghost int

class Obj_Ghost:
    def __init__(self, ghost_name, shape):
        self.name = ghost_name # ghost1, ghost2, ghost3 string
        self.cells = shape # [(0,0),(1,0),(2,0),(3,0),(4,0)] a list of locations on the board
        self.state = Ghost # Ghost, Solid, Dead string

class main:
    def __init__(self):
        self.blocks = Blocks() # load the shapes of all the blocks
        self.objects = [] # a list of block objects
        self.board = [] # 2d list where each col is list of ghost names that are located there
        self.ghost_index = 0

        #### TEST ####
        self.setup_board(3)
        self.create_object(self.blocks.Orange)
        self.create_object(self.blocks.Brown)
        self.create_object(self.blocks.Green)
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
        # run a for loop throgh the board
        r = 0
        c = 0
        block = Obj_Block()
        self.objects.append(block)
        for row in self.board: # row = [[],[],[]]
            for col in row: # col = []
                # now place ghosts of the object in all its angles
                name = ""
                for angle, cells in obj_block.items(): # angle: Name, 0, 1, 2, 3, 4, cells: "Orange", ((0,0),(0,1),(1,0),(2,0),(3,0))
                    if angle != "Name":
                        fail = False
                        shape = []
                        # go over each cell ((0,0),(0,1),(1,0),(2,0),(3,0))
                        for cell in cells:
                            roffset = r+cell[0]
                            coffset = c+cell[1]

                            # try to see if this offset is within the borders of the board
                            try:
                                test = self.board[roffset][coffset]
                                shape.append((roffset,coffset))
                            except:
                                fail = True
                                shape = []
                        
                        # after the set ((0,0),(0,1),(1,0),(2,0),(3,0)) is placed on the board, if it succeeded 
                        if not fail:
                            # the shape if a set of:
                            # print("r=",r,"c=",c,"angle=",angle,"shape=",shape)
                            # r= 0 c= 0 angle= 0 shape= [(0, 0), (0, 1), (1, 0), (2, 0), (3, 0)]
                            # create a ghost nd insert it into the block object
                            self.ghost_index += 1
                            ghost = Obj_Ghost(self.ghost_index, shape)
                            block.ghosts.append(ghost)
                            for cell in shape:
                                self.board[cell[0]][cell[1]].append(self.ghost_index)
                    else:
                        name = cells
                        block.color = name
                # add cell
                c += 1
            # add row
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
                for cell in col:
                    display += "G"+str(cell)+" "
                display += "|"
            display += "\n"
        print(display)

main()