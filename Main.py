print("loading...")

import RPi.GPIO as g
import time as t
import serial as s
import struct as st
from picamera import PiCamera

import CameraSensorManagement as csm
import DisplayManagement as dm
import DatabaseManagement as dbm

import LcdDriver as lcdr

g.cleanup()

# define constants for display management
V_SOURCE = 0
W_TITLE = "Camera Display"
CPOSX = 0
CPOSY = 0

#define constants for database management
HOST = 'accesssecuritysystem.cxa5ja6qsxdg.us-east-2.rds.amazonaws.com'
USER = 'miles'
PASS = 'as210!0!'
DB = 'access'
PORT = 3306

# define pins
LED_RED = 40
LED_GRN = 38

PIR = 11

class Main:
    
    def allow_access(self, msg = "Welcome"):
        # enable / disable relative leds
        g.output(LED_GRN, g.HIGH)
        g.output(LED_RED, g.LOW)
        t.sleep(2)
        g.output(LED_GRN, g.LOW)
        
        # display message on LCD
        # self.lcd.lcd_display_string(msg, 1)
        
        # add access to database
        
    def deny_access(self, msg = "'I'll hunt you down, and gut you like a fish!'"):
        # enable / disable relative leds
        g.output(LED_RED, g.HIGH)
        g.output(LED_GRN, g.LOW)
        t.sleep(2)
        g.output(LED_RED, g.LOW)
        
        # display message on LCD
        # self.lcd.lcd_display_string(msg, 1)
        
        # add access to database
    
    def loop(self):
        while(True):
            sel = input("\nPlease select: \n(1) Enrol Face\n(2) Verify Face\n")
            if (sel is "1"):
                name = input("Please enter a name for the enrollment: ")
                self.camera.enrol_face(name, self.db)
            elif (sel is "2"):
                while(True):
                    if (g.input(PIR) == g.HIGH):
                        print("Looking for faces...")
                        result, rs = self.camera.scan_for_faces()
                        if result:
                            print("Matching faces...")
                            result = self.camera.compare_with_database(self.db, c_rs = rs)
                            if result:
                                print("Match found!")
                                self.allow_access()
                                break;
                            else:
                                print("No match found!")
                                self.deny_access()
                                break;
                        print("No faces found!")
                        break;
                            
    def test_modules(self):
        # Test the system can connect to the database
        conn = self.db.connect()
        if (conn is None):
            return False
        else:
            conn.close()
            return True
    
    def setup(self):
        # setup pinmode
        g.setmode(g.BOARD)

        # setup LED pins
        g.setup(LED_RED, g.OUT)
        g.setup(LED_GRN, g.OUT)
        
        # setup PIR Motion pins
        g.setup(PIR, g.IN)
        
    def start(self):
        self.setup()

        # lcd = lcdr.lcd()
        # lcd.lcd_display_string("Test", 1)
        # self.lcd = lcd

        # open display
        display = dm.Display(W_TITLE, CPOSX, CPOSY, V_SOURCE)
        display.start()
        self.display = display
                
        # set default values for LEDs
        g.output(LED_RED, g.LOW)
        g.output(LED_GRN, g.LOW)
        
        # wait for the display to complete initializing
        print("initializing...")
        t.sleep(2)
        
        # create camera object
        camera = csm.Camera(self.display)
        self.camera = camera
        
        # create database object
        db = dbm.Database(HOST, PORT, USER, PASS, DB)
        self.db = db
        
        # conduct startup tests
        test = self.test_modules()
        if (test is True):
            # begin main loop
            print("starting...")
            self.loop()
        else:
            print("Tests failed, trying again")
            self.start()
        
    def __del__(self):
        g.cleanup()

main = Main()
main.start()