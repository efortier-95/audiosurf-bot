import win32api
import win32con
import cv2 as cv
from random import randint


class Bot:

    def __init__(self):
        # Load trained models
        self.block_cascade = cv.CascadeClassifier(r'cascade_block\cascade.xml')
        self.spike_cascade = cv.CascadeClassifier(r'cascade_spike\cascade.xml')

        # Ship center coordinates
        self.ship_x = 310
        self.ship_y = 375

        # Ship position flags
        self.center = True
        self.left = False
        self.right = False

        # Keyboard hex codes
        self.a = 0x41
        self.d = 0x44

    def hold_left(self):
        """Hold down 'a' key"""
        win32api.keybd_event(self.a, 0, 0, 0)

    def hold_right(self):
        """Hold down 'd' key"""
        win32api.keybd_event(self.d, 0, 0, 0)

    def release(self):
        """Release both 'a' and 'd' key"""
        win32api.keybd_event(self.a, 0, win32con.KEYEVENTF_KEYUP, 0)
        win32api.keybd_event(self.d, 0, win32con.KEYEVENTF_KEYUP, 0)

    @staticmethod
    def get_click_points(rectangles):
        """Convert [x, y, w, h] rectangles from 
        cascade detection to [x, y] center positions
        """
        points = []
        for (x, y, w, h) in rectangles:
            
            # Determine the center position
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            points.append((center_x, center_y))

        return points

    def hit_block(self, screenshot):
        """Calculate distance of incoming blocks
        and move to those when they are close
        """
        detect_block = self.block_cascade.detectMultiScale(screenshot)

        if len(detect_block) > 0:
            blocks = self.get_click_points(detect_block)

            for block in blocks:
                block_x, block_y = block

                # Distance from block to ship
                bx = block_x - self.ship_x
                by = abs(self.ship_y - block_y)

                if by < 75:
                    # Left block
                    if bx < -15:
                        if self.center:
                            self.hold_left()
                            self.left = True
                            self.center = False
                        elif self.right:
                            self.release()
                            self.right = False
                            self.center = True
                    # Right block
                    elif bx > 15:
                        if self.center:
                            self.hold_right()
                            self.right = True
                            self.center = False
                        elif self.left:
                            self.release()
                            self.left = False
                            self.center = True

    def dodge_spike(self, screenshot):
        """Calculate distance of incoming spikes
        and move to another lane to dodge them
        """
        detect_spike = self.spike_cascade.detectMultiScale(screenshot)

        if len(detect_spike) > 0:
            spikes = self.get_click_points(detect_spike)

            for spike in spikes:
                spike_x, spike_y = spike

                # Distance from spike to ship
                sx = spike_x - self.ship_x
                sy = abs(self.ship_y - spike_y)

                if sy < 125:
                    # Center spike
                    if -15 <= sx <= 15:
                        if self.center:
                            # Randomly move left or right if ship is already centered
                            move = randint(0, 1)
                            if move == 0:
                                self.hold_left()
                                self.left = True
                            elif move == 1:
                                self.hold_right()
                                self.right = True
                            self.center = False
                    # Left spike
                    elif sx < -20:
                        if self.left:
                            self.release()
                            self.left = False
                            self.center = True
                    # Right spike
                    elif sx > 20:
                        if self.right:
                            self.release()
                            self.right = False
                            self.center = True
