import tkinter as tk
import cv2
from threading import Thread
from PIL import Image, ImageTk

class Display(Thread):
    
    def __init__(self, w_title, cposx, cposy, source = 0):
        
        # initialize the Thread class
        Thread.__init__(self)
        
        # define an instance attribute fro the parameters
        self.W_TITLE = w_title
        self.CPOSX = cposx
        self.CPOSY = cposy
        self.source = source
        
    def run(self):        
        # define the window object and set the window title
        self.window = tk.Tk()
        self.window.title(self.W_TITLE)
        
        # define a video capture from the source passed in to the constructor
        self.v = cv2.VideoCapture(self.source)
        
        # check if the video capture connection was opened with the source.
        if not self.v.isOpened():
            print(format("Unable to open stream from source {}", source))
            
        # store the width and height of the video source
        self.c_width = self.v.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.c_height = self.v.get(cv2.CAP_PROP_FRAME_HEIGHT)

        # create the canvas widget from displaying each frame
        self.canvas = tk.Canvas(self.window, width = self.c_width, height = self.c_height)
        self.canvas.pack()

        # define the delay of frame refresh
        self.u_delay = 10
                
        # update the screen
        self.update()
        
        self.window.mainloop()
        
    def get_frame(self):
        # check if the video stream is opened
        if self.v.isOpened():
            # read a frame from the video source
            retval, frame = self.v.read()
            
            # if there was a frame to be read in the stream, return it as
            # an rgb image
            if retval:
                return (retval, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (retval, none)
        
    def update(self):
        # get an image frame from the video source
        retval, frame = self.get_frame()
        
        # set current frame (acts as a screenshot for other classes requiring the rpi camera to use)
        self.cur_frame = frame
        
        # draw an image of the above frame on the canvas
        if retval:
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            self.canvas.create_image(self.CPOSX, self.CPOSY, image = self.photo, anchor = tk.NW)
            
        self.window.after(self.u_delay, self.update)   
    
    def __del__(self):
        if (self.v.isOpened()):
            self.v.release()