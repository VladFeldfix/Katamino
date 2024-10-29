from Blocks import Blocks
import tkinter
from tkinter import *
import os
from PIL import ImageTk, Image
import threading
from tkinter import messagebox
from datetime import datetime
from collections import deque # for BFS in flood fill algorithm


Ghost = "Ghost"
Solid = "Solid"
Dead = "Dead"

class Obj_Block:
    def __init__(self):
        self.color = "" # Blue, Orange, Grey string
        self.ghosts = [] # [ghost1, ghost2, ghost3] a list of ghost objects
        self.selected_ghost = 0 # the index of the solid ghost int

class Obj_Ghost:
    def __init__(self, ghost_name, shape, tag, x, y):
        self.name = ghost_name # ghost1, ghost2, ghost3 string
        self.cells = shape # [(0,0),(1,0),(2,0),(3,0),(4,0)] a list of locations on the board
        self.state = Ghost # Ghost, Solid, Dead string
        self.tag = tag
        self.x = x
        self.y = y

class main:
    def __init__(self):
        # global variables
        self.blocks = Blocks() # load the shapes of all the blocks
        self.objects = {} # a dict of block objects with name for selecting
        self.ghosts = {} # a list of ghosts objects for refernce (for collision code)
        self.object_list = [] # a list of objects id's to reference the self.objects dictionary
        self.board = [] # 2d list where each col is list of ghost names that are located there
        self.ghost_index = 0
        self.animation = {}
        self.steps = 0

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
        self.W = 320*4
        self.H = 240*3
        root.geometry(str(self.W)+"x"+str(self.H))
        root.minsize(self.W,self.H)
        root.title("Katamino v1.0")
        root.iconbitmap("favicon.ico")
        for x in range(12):
            root.columnconfigure(x, weight=1)
        root.rowconfigure(0, weight=1)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=1)
        root.resizable(False, False)

        # setup canvas
        self.canvas = Canvas(root, width=self.W, height=self.H-50, bg="white")
        self.canvas.grid(row=0, column=0, columnspan=13, sticky="WN")

        # setup graphical board
        image = Image.open("Board/board.png")
        photoimage = ImageTk.PhotoImage(image)
        sprites.append(photoimage)
        self.boardx = 158
        self.boardy = 61
        self.canvas.create_image(0, 0, image = photoimage, anchor=NW)

        # setup graphical board devider
        image = Image.open("Board/board_devider.png")
        photoimage = ImageTk.PhotoImage(image)
        sprites.append(photoimage)
        self.canvas.create_image(self.boardx+64*4, self.boardy, image = photoimage, anchor=NW, tag="Devider")

        # setup graphical board buttons
        for i in range(3,13):
            image = Image.open("Board/board_button_"+str(i).zfill(2)+".png")
            photoimage = ImageTk.PhotoImage(image)
            sprites.append(photoimage)
            Tag = "board_btn"+str(i)
            self.canvas.create_image(self.boardx+64+(64*i), self.boardy, image = photoimage, anchor=NW, tag=Tag)
            self.canvas.tag_bind(Tag, "<Enter>", lambda event: self.check_hand_enter())
            self.canvas.tag_bind(Tag, "<Leave>", lambda event: self.check_hand_leave())
            self.canvas.tag_bind(Tag, "<ButtonPress-1>", lambda event: self.setup_board(self))
        
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
                    self.canvas.create_image(self.W+10, self.H+10, image = photoimage, anchor=NW, tag=file.replace(".png", ""))

                    # add block activation button
                    number = file[0:2]
                    if number != lastname:
                        lastname = number
                        name = filename.replace("_1.png","")
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

        # steps
        self.start_time = ""
        self.end_time = ""
        self.steps_and_timestamp = "Steps: "+f"{self.steps:,}"+"  Start time: "+self.start_time+"  End time: "+self.end_time
        self.steps_text = self.canvas.create_text(self.boardx,self.boardy+64*7+32,text=self.steps_and_timestamp,fill="black",font="Arial 20 bold",anchor="w")

        # help
        image = Image.open("Buttons/help.png")
        photoimage = ImageTk.PhotoImage(image)
        sprites.append(photoimage)
        Tag = "help"
        self.canvas.create_image(0,0, image = photoimage, anchor=NW, tag=Tag)
        self.canvas.tag_bind(Tag, "<Enter>", lambda event: self.check_hand_enter())
        self.canvas.tag_bind(Tag, "<Leave>", lambda event: self.check_hand_leave())
        self.canvas.tag_bind(Tag, "<ButtonPress-1>", self.help)

        # run main loop
        root.mainloop()
    
    def press_button(self, data):
        if not self.playing:
            btn = data[0]
            tkinter_button_object = data[1]
            btn = btn.split("_")
            btn[0] = btn[0].replace("\\", "/")
            tmp = btn[0].split("/")
            btn = tmp[1]+"_"+btn[1]
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
        self.start_time = timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.steps_and_timestamp = "Steps: "+f"{self.steps:,}"+"  Start time: "+self.start_time+"  End time: "+self.end_time
        self.canvas.itemconfigure(self.steps_text, text=self.steps_and_timestamp)
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
            self.steps += 1
            self.steps_and_timestamp = "Steps: "+f"{self.steps:,}"+"  Start time: "+self.start_time+"  End time: "+self.end_time
            self.canvas.itemconfigure(self.steps_text, text=self.steps_and_timestamp)
            goto_next = False
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
                goto_next = True
            
            # we shouldn't do these checks if we already know we're gonna go to next
            if (not goto_next):
                # test board for dead spots
                for row in self.board:
                    for col in row:
                        deadcell = True
                        for ghost_id in col:
                            ghost = self.ghosts[ghost_id]
                            if ghost.state != Dead:
                                deadcell = False
                                break # no need to keep checking because we found it isn't dead
                        if deadcell:
                            goto_next = True
                            break
                
                
                # test for a non multiple of 5 hole, which is impossible to fill
                
                # here we create an array of booleans, one for each position on the board.
                # they start at False because we have yet to visit any of them, when we do they'll change to True
                visited = [[False]* len(self.board[0]) for i in range(5) ] # create a 5 by whatever width they picked array
                added_cells = block.ghosts[block.selected_ghost].cells # these are the cells that were added by solidifying this ghost
                
                for y,x in added_cells:
                    visited[y][x] = True # makes it a bit faster, by exiting from the while quickly
                
                for modified_cell in added_cells:
                    count = 0
                    BFS_queue = deque([modified_cell]) # this is the first cell to look at
                    while BFS_queue: # while there are more items in the queue
                        y, x = BFS_queue.popleft()
                        
                        # add neighbors to queue
                        for pos in ( (y-1,x),(y+1,x), (y,x-1),(y,x+1) ): # the four directions
                            if pos[0]<0 or pos[0] >= 5 or pos[1]<0 or pos[1] >= len(self.board[0]) : # out of range
                                continue
                            
                            if visited[pos[0]][pos[1]]:
                                continue # we've already reached this position
                            
                            # make sure the cell is empty
                            is_empty = True
                            for ghost_id in self.board[pos[0]][pos[1]]:
                                ghost = self.ghosts[ghost_id]
                                if ghost.state == Solid:
                                    is_empty = False
                                    break
                            if not is_empty:
                                continue
                            
                            # we found a new empty neighbor so we add it to the queue and add to the count
                            BFS_queue.append(pos)
                            count += 1
                            visited[pos[0]][pos[1]] = True
                    
                    if count % 5 != 0: # if a hole has a non multiple of 5 number of cells, then it can't be filled
                        goto_next = True
                        break
                
                
            
            # next
            if goto_next:
                # if reached a dead end adjustment are needed
                # step 1: make all ghosts Ghosts
                self.reset_all_ghosts()

                # step 2: delete the last step
                try:
                    winpath.pop()
                except:
                    # unsolvable
                    self.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    self.steps_and_timestamp = "Steps: "+f"{self.steps:,}"+"  Start time: "+self.start_time+"  End time: "+self.end_time
                    self.canvas.itemconfigure(self.steps_text, text=self.steps_and_timestamp)
                    messagebox.showerror("Error","This combination cannot be solved!")
                    break
                self.objects[self.object_list[pointer]].selected_ghost = 0

                # step 3: pointer go back in the last block and +1 in the previous
                pointer -= 1
                self.objects[self.object_list[pointer]].selected_ghost +=1

                # step 4: refill the solids
                for step in winpath:
                    obj = self.objects[step[0]]
                    self.make_ghost_solid(obj.ghosts[obj.selected_ghost])

            # update animation
            self.update_animation()

        # update animation lasat time before winning
        self.steps_and_timestamp = "Steps: "+f"{self.steps:,}"+"  Start time: "+self.start_time+"  End time: "+self.end_time
        self.canvas.itemconfigure(self.steps_text, text=self.steps_and_timestamp) 
        self.update_animation()

        # end
        if win:
            # test board for dead spots
            empty_spaces = False
            for row in self.board:
                for col in row:
                    if len(col) > 0:
                        for ghost_id in col:
                            ghost = self.ghosts[ghost_id]
                            if ghost.state == Ghost:
                                empty_spaces = True
                    else:
                        empty_spaces = True
            if not empty_spaces:
                self.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.steps_and_timestamp = "Steps: "+f"{self.steps:,}"+"  Start time: "+self.start_time+"  End time: "+self.end_time
                self.canvas.itemconfigure(self.steps_text, text=self.steps_and_timestamp)
                messagebox.showinfo("Info","Complete!")
                
            else:
                self.end_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                self.steps_and_timestamp = "Steps: "+f"{self.steps:,}"+"  Start time: "+self.start_time+"  End time: "+self.end_time
                self.canvas.itemconfigure(self.steps_text, text=self.steps_and_timestamp)
                messagebox.showerror("Error","This combination cannot be solved!")

    def make_ghost_solid(self, obj_ghost):
        if obj_ghost.state != Dead:
            this_id = obj_ghost.name
            obj_ghost.state = Solid
            self.animation[obj_ghost.tag] = (obj_ghost.x, obj_ghost.y) #self.canvas.coords(obj_ghost.tag, obj_ghost.x, obj_ghost.y)
            
            # kill every ghost that is touching my ghost
            for cell in obj_ghost.cells:
                r = cell[0]
                c = cell[1]
                selected_board_cell = self.board[r][c] # # selected_board_cell > [1, 3, 4, 17, 20, 33, 36]
                for ghost_id in selected_board_cell: # kill all ghosts coliding with the solid ghost
                    if ghost_id != this_id: # dont kill yourself
                        self.ghosts[ghost_id].state = Dead # kill ghost on collision
            
            # kill all the ghosts of the same objcet
            tag = obj_ghost.tag # 04_Purple_2
            tag = tag.split("_")
            tag = tag[0]+"_"+tag[1]
            block = self.objects[tag] # this will be block = Obj_block
            for gh in block.ghosts:
                if gh.name != obj_ghost.name:
                    gh.state = Dead

    
    def reset_all_ghosts(self):
        for ghost in self.ghosts.values():
            ghost.state = Ghost
            self.animation[ghost.tag] = (self.W+10, self.H+10)
            #self.canvas.coords(ghost.tag, self.W+10, self.H+10)
    
    def update_animation(self):
        for block, coordinates in self.animation.items():
            self.canvas.coords(block, coordinates[0], coordinates[1])

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
                            tag = name+"_"+str(angle+1)
                            x = c*64+self.boardx+64
                            y = r*64+self.boardy+64
                            #print(tag)
                            ghost = Obj_Ghost(self.ghost_index, shape, tag, x, y)
                            #self.canvas.coords(tag, x, y)
                            #input(self.board)
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
            self.canvas.coords("Devider", self.boardx+64+(64*size), self.boardy)
            self.board = []
            for row in range(5):
                self.board.append([])
                for _ in range(size):
                    self.board[row].append([])\
    
    def help(self, event):
        os.popen("help.pdf")

main()