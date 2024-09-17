from Blocks import Blocks

Ghost = "Ghost"
Solid = "Solid"
Dead = "Daed"

class object:
    def __init__(self, index, cells, name, state):
        self.index = index
        self.cells = cells
        self.name = name
        self.state = state

class main:
    def __init__(self):
        self.blocks = Blocks()
        self.board = []
        self.objects = {}
        self.indexes = []
        self.index = 0

        ### TEST ###
        self.setup_board(3)
        self.add_object_to_game(self.blocks.Orange)
        self.add_object_to_game(self.blocks.Brown)
        self.add_object_to_game(self.blocks.Green)
        self.display_board()
        self.calculate()
        ############

    def calculate(self):
        current_color = ""
        win = False
        winarr = []
        forbidden_places = {} # this library indicates what object cannot be at what winarr index
        pointer = 0
        while not win:
            print("\nCalculate:")
            pointer = 0
            for index in self.indexes:
                # point at the next object
                obj = self.objects[index]

                # determine if an object can be selected
                can_select = True
                if current_color == obj.name:
                    can_select = False
                
                if obj.state != Ghost:
                    can_select = False
                print("obj.index",obj.index,forbidden_places)
                if obj.index in forbidden_places:
                    print("obj.index in forbidden_places")
                    if len(winarr) == forbidden_places[obj.index]:
                        can_select = False
                        print("len(winarr) == forbidden_places[obj.index]",len(winarr),obj.index)

                # select the object and make it solid
                if can_select:
                    winarr.append(index)
                    obj.state = Solid
                    current_color = obj.name
                    for cell in obj.cells:
                        r = cell[0]
                        c = cell[1]
                        row = self.board[r][c]
                        for indx in row:
                            select = self.objects[indx]
                            if select.index != obj.index:
                                select.state = Dead
                    
                pointer += 1
            
            # test for win
            win = True
            for row in self.board:
                for col in row:
                    for index in col:
                        obj = self.objects[index]
                        if obj.state != Solid:
                            win = False
            print(winarr)
            self.display_board()
            # remove the last element from winarr
            index = winarr.pop()
            forbidden_places[index] = len(winarr)
            print(forbidden_places)

            # renew board
            for index in self.indexes:
                self.objects[index].state = Ghost
            
            input(winarr) # for testing
            winarr = []
            #win = True # for testing

    def add_object_to_game(self, obj_block):
        r = 0
        c = 0
        for row in self.board:
            for col in row:
                name = ""
                for angle, cells in obj_block.items():
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
                            index = self.index
                            self.index += 1
                            self.objects[index] = (object(index, shape, name, Ghost))
                            self.indexes.append(index)
                            for cell in shape:
                                placerow = cell[0]
                                placecol = cell[1]
                                self.board[placerow][placecol].append(index)
                    name = obj_block["Name"]
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
        r = 0
        c = 0
        for row in self.board:
            display += "|"
            for col in row:
                score = 0
                for index in col:
                    if self.objects[index].state != Dead:
                        score += 1
                if score > 1:
                    display += str(score).zfill(10)+"|"
                elif score == 1:
                    select = self.objects[self.board[r][c][0]]
                    if select.state == Solid:
                        show = select.name
                        addthis = str(show).zfill(10)+"|"
                        display += addthis.replace("0", " ")
                    else:
                        display += "1".zfill(10)+"|"
                elif score == 0:
                    display += "0".zfill(10)+"|"
                c += 1
            display += "\n"
            c = 0
            r += 1
        print("BOAD:")
        print(display)
        for row in self.board:
            print(row)
        print("\nOBJECTS:")
        for index, obj in self.objects.items():
            print(index, obj.index, obj.name, obj.cells, obj.state)

main()