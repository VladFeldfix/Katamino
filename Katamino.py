from Blocks import Blocks

Ghost = "Ghost"
Solid = "Solid"
Dead = "Dead"

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
        self.objects = {} # a dict of block objects with name for selecting
        self.ghosts = {} # a list of ghosts objects for refernce (for collision code)
        self.object_list = [] # a list of objects id's to reference the self.objects dictionary
        self.board = [] # 2d list where each col is list of ghost names that are located there
        self.ghost_index = 0

        #### TEST ####
        self.setup_board(3)
        self.create_object(self.blocks.Orange)
        self.create_object(self.blocks.Brown)
        self.create_object(self.blocks.Green)
        self.make_ghost_solid(self.objects["Orange"].ghosts[0])
        self.reset_all_ghosts()
        #self.display_board()
        self.calculate()
        ##############

    def calculate(self):
        # the calculation method:
        # START LOOP
        # go to next object in self.objects (start from 0)
        # set the objects' selected_ghost proparty to the next index (start from 0)
        # go to the next object in the list self.objects
        # select the first available ghost and set selected_ghost to the index of the ghost
        # if there are no available shosts at go back to the prev self.objects index and goto START LOOP
        
        win = False
        pointer = 0
        winpath = []
        while not win:
            # select a block acording to the pointer location
            block = self.objects[self.object_list[pointer]] # self.object_list = ['Orange', 'Brown', 'Green'], block > Obj_Block()
    
            ###########  display for testing  ###########
            display = ""
            i = 0
            for name in self.object_list:
                BLOCK = self.objects[name]
                if pointer == i:
                    this = ">"
                else:
                    this = ""
                display += this+BLOCK.color+": [selected:"+str(BLOCK.selected_ghost)+"]"
                for ghost in BLOCK.ghosts:
                    display += " "+str(ghost.name)+"-"+ghost.state
                display += "\n"
                i += 1
            print("START OF TURN:")
            print(display)
            print(winpath)
            #############################################

            # find the fist available ghost and make it solid
            ghost = None
            deadend = False
            while ghost == None:
                if block.selected_ghost < len(block.ghosts):
                    if block.ghosts[block.selected_ghost].state == Ghost:
                        ghost = block.ghosts[block.selected_ghost] # ghost -> Obj_Ghost()
                        self.make_ghost_solid(ghost)
                        winpath.append((block.color, block.selected_ghost))
                    else:
                        block.selected_ghost += 1
                else:
                    deadend = True
                    break
            
            if not deadend:
                if pointer < len(self.object_list)-1:
                    pointer += 1
                else:
                    win = True
                    print('WIN')
                    self.display_board()
            else:
                print("DEADEND!!")
                # if reached a dead end adjustment are needed
                # step 1: make all ghosts Ghosts
                self.reset_all_ghosts()

                # step 2: delete the last step
                winpath.pop()
                self.objects[self.object_list[pointer]].selected_ghost = 0

                # step 3: pointer go back in the last block and +1 in the previous
                pointer -= 1
                self.objects[self.object_list[pointer]].selected_ghost +=1

                # step 4: refill the solids
                for step in winpath:
                    obj = self.objects[step[0]]
                    self.make_ghost_solid(obj.ghosts[obj.selected_ghost])

            ###########  display for testing  ###########
            display = ""
            i = 0
            for name in self.object_list:
                BLOCK = self.objects[name]
                if pointer == i:
                    this = ">"
                else:
                    this = ""
                display += this+BLOCK.color+": [selected:"+str(BLOCK.selected_ghost)+"]"
                for ghost in BLOCK.ghosts:
                    display += " "+str(ghost.name)+"-"+ghost.state
                display += "\n"
                i += 1
            print("END OF TURN:")
            print(display)
            print(winpath)
            #############################################
            input("------------------------------------------------------------------------------------------->")

    def make_ghost_solid(self, obj_ghost):
        if obj_ghost.state != Dead:
            this_id = obj_ghost.name
            obj_ghost.state = Solid
            for cell in obj_ghost.cells:
                r = cell[0]
                c = cell[1]
                selected_board_cell = self.board[r][c] # print(selected_board_cell) > [1, 3, 4, 17, 20, 33, 36]
                for ghost_id in selected_board_cell: # kill all ghosts coliding with the solid ghost
                    if ghost_id != this_id: # dont kill yourself
                        self.ghosts[ghost_id].state = Dead # kill ghost on collision
    
    def reset_all_ghosts(self):
        for ghost in self.ghosts.values():
            ghost.state = Ghost
    
    def create_object(self, obj_block):
        # run a for loop throgh the board
        r = 0
        c = 0
        block = Obj_Block()
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
                            self.ghosts[self.ghost_index] = ghost
                            for cell in shape:
                                self.board[cell[0]][cell[1]].append(self.ghost_index)
                    else:
                        name = cells
                        block.color = name
                        if not name in self.objects:
                            self.objects[name] = block
                            self.object_list.append(name)
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
                    display += "G"+str(cell)+" "+self.ghosts[cell].state+","
                display += "|"
            display += "\n"
        print(display)

main()