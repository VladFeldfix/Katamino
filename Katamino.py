from Blocks import Blocks
import tkinter
from tkinter import *
import os
from PIL import ImageTk, Image
import threading

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
        # global variables
        self.blocks = Blocks() # load the shapes of all the blocks
        self.objects = {} # a dict of block objects with name for selecting
        self.ghosts = {} # a list of ghosts objects for refernce (for collision code)
        self.object_list = [] # a list of objects id's to reference the self.objects dictionary
        self.board = [] # 2d list where each col is list of ghost names that are located there
        self.ghost_index = 0

        # setup board initial
        for row in range(5):
            self.board.append([])
            for _ in range(3):
                self.board[row].append([])

        # activate gui
        self.activate_gui()
    
    def activate_gui(self):
        # set variables
        sprites = []
        self.buttons = []
        self.activation_list = []
        self.playing = False
        
        # setup main window
        root = tkinter.Tk()
        W = 320*4
        H = 240*3
        root.geometry(str(W)+"x"+str(H))
        root.minsize(W,H)
        root.title("Katamino v1.0")
        #root.iconbitmap("favicon.ico")
        for x in range(12):
            root.columnconfigure(x, weight=1)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)
        root.resizable(False, False)

        # setup canvas
        self.canvas = Canvas(root, width=W, height=H-50, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=13, sticky="WN")

        # setup graphical board
        image = Image.open("Board/board.png")
        photoimage = ImageTk.PhotoImage(image)
        sprites.append(photoimage)
        self.boardx = 64
        self.boardy = 64
        self.canvas.create_image(self.boardx, self.boardy, image = photoimage, anchor=NW)

        # setup graphical board buttons
        for i in range(3,13):
            image = Image.open("Board/board_button_"+str(i).zfill(2)+".png")
            photoimage = ImageTk.PhotoImage(image)
            sprites.append(photoimage)
            Tag = "board_btn"+str(i)
            self.canvas.create_image(self.boardx+32+(32*i), self.boardy, image = photoimage, anchor=NW, tag=Tag)
            self.canvas.tag_bind(Tag, "<Enter>", lambda event: self.check_hand_enter())
            self.canvas.tag_bind(Tag, "<Leave>", lambda event: self.check_hand_leave())
            self.canvas.tag_bind(Tag, "<ButtonPress-1>", lambda event: self.setup_board(self))
        
        # setup graphical board devider
        image = Image.open("Board/board_devider.png")
        photoimage = ImageTk.PhotoImage(image)
        sprites.append(photoimage)
        self.canvas.create_image(self.boardx+128, self.boardy, image = photoimage, anchor=NW, tag="Devider")
        
        # setup blocks
        lastname = ""
        x = 0
        for path, directories, files in os.walk('Blocks'):
            for file in files:
                if ".png" in file:
                    # add block
                    filename = path+"/"+file.replace("\\","/")
                    image = Image.open(filename)
                    photoimage = ImageTk.PhotoImage(image)
                    sprites.append(photoimage)
                    self.canvas.create_image(W+10, H+10, image = photoimage, anchor=NW, tag=file.replace(".png", ""))

                    # add block activation button
                    number = file[0:2]
                    if number != lastname:
                        lastname = number
                        name = file[3:].replace("_1.png","")
                        image = Image.open("Buttons/"+lastname+".png")
                        image = image.resize((103,97), Image.LANCZOS)
                        resizedimage = ImageTk.PhotoImage(image)
                        sprites.append(resizedimage)
                        btn = Button(root, image = resizedimage, height=200)
                        btn.config(command=lambda fn=(filename, btn): self.press_button(fn))
                        btn.grid(column=x, row=1, sticky="NEWS")
                        self.buttons.append(btn)
                        x += 1

        # setup start button
        start_button = Button(root, height=2, text="START", command=self.start)
        start_button.grid(row=3, column=0, columnspan=13, sticky="NEWS")
        self.buttons.append(start_button)

        # run main loop
        root.mainloop()
    
    def press_button(self, data):
        if not self.playing:
            btn = data[0]
            tkinter_button_object = data[1]
            btn = btn.split("_")
            btn = btn[1]
            add = self.blocks.activation_list[btn]
            if not add in self.activation_list:
                self.activation_list.append(add)
                tkinter_button_object.config(bg = "black")
            else:
                self.activation_list.remove(add)
                tkinter_button_object.config(bg = self.RGB((240,240,240)))

    def RGB(self, color):
        return "#%02x%02x%02x" % color

    def start(self):
        if not self.playing:
            if len(self.activation_list) > 0:
                # disable all buttons
                self.playing = True
                for button in self.buttons:
                    button.config(state=DISABLED)

                # set self.activation_list
                for iten in self.activation_list:
                    self.create_object(iten)

                # start calculator
                self.thread = threading.Thread(target=self.calculate)
                self.thread.daemon = True
                self.thread.start()

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
            else:
                # if reached a dead end adjustment are needed
                # step 1: make all ghosts Ghosts
                self.reset_all_ghosts()

                # step 2: delete the last step
                try:
                    winpath.pop()
                except:
                    # unsolvable
                    break
                self.objects[self.object_list[pointer]].selected_ghost = 0

                # step 3: pointer go back in the last block and +1 in the previous
                pointer -= 1
                self.objects[self.object_list[pointer]].selected_ghost +=1

                # step 4: refill the solids
                for step in winpath:
                    obj = self.objects[step[0]]
                    self.make_ghost_solid(obj.ghosts[obj.selected_ghost])

    def make_ghost_solid(self, obj_ghost):
        if obj_ghost.state != Dead:
            this_id = obj_ghost.name
            obj_ghost.state = Solid
            for cell in obj_ghost.cells:
                r = cell[0]
                c = cell[1]
                selected_board_cell = self.board[r][c] # # selected_board_cell > [1, 3, 4, 17, 20, 33, 36]
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
                            # "r=",r,"c=",c,"angle=",angle,"shape=",shape
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

    def check_hand_enter(self):
        if not self.playing:
            self.canvas.config(cursor="hand2")

    def check_hand_leave(self):
        self.canvas.config(cursor="")

    def setup_board(event, self):
        if not self.playing:
            size = self.canvas.gettags("current")[0]
            size = size.replace("board_btn","")
            size = int(size)
            self.canvas.coords("Devider", self.boardx+32+(32*size), self.boardy)
            self.board = []
            for row in range(5):
                self.board.append([])
                for _ in range(size):
                    self.board[row].append([])

main()