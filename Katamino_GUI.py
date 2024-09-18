import tkinter
from tkinter import *
from tkinter import font as tkfont
from PIL import ImageTk, Image
from tkinter import filedialog
import os
import random
from Katamino import main
import sys

class GUI:
    def __init__(self):
        # global variables
        sprites = []
        katamino = main()
        
        # setup main window
        root = tkinter.Tk()
        root.geometry("640x480")
        root.minsize(640,480)
        root.title("Katamino v1.0")
        #root.iconbitmap("favicon.ico")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        # setup self.canvas
        self.canvas = Canvas(root, width=640, height=480, bg="white")
        self.canvas.grid(row=0, column=0)

        # load images
        for path, directories, files in os.walk('Blocks'):
            for file in files:
                if ".png" in file:
                    filename = path+"/"+file.replace("\\","/")
                    image = Image.open(filename)
                    photoimage = ImageTk.PhotoImage(image)
                    sprites.append(photoimage)
                    self.canvas.create_image(650, 490, image = photoimage, anchor=NW, tag=file.replace(".png", ""))
                    #self.canvas.coords("01_Navy_1", 200, 200)
        # run main loop
        root.mainloop()
    
    def place_block(self, block_name, y, x):
        self.canvas.coords(block_name, y, x)

GUI()