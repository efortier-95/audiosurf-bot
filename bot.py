import cv2 as cv
from keyboard import Keyboard
from random import randint


class Bot:

    def __init__(self):
        self.block_cascade = cv.CascadeClassifier(r'cascade_block\cascade.xml')
        self.spike_cascade = cv.CascadeClassifier(r'cascade_spike\cascade.xml')

        # Ship center coordinates
        self.ship_x = 310
        self.ship_y = 375

        # Ship position flags
        self.center = True
        self.left = False
        self.right = False

        self.kb = Keyboard()

    # Convert [x, y, w, h] to [x, y] center positions
    @staticmethod
    def get_click_points(rectangles):
        points = []

        # Loop over all the rectangles
        for (x, y, w, h) in rectangles:
            # Determine the center position
            center_x = x + int(w/2)
            center_y = y + int(h/2)
            # Save the points
            points.append((center_x, center_y))

        return points

    def dodge_spike(self, screenshot):
        detect_spike = self.spike_cascade.detectMultiScale(screenshot)

        if len(detect_spike) > 0:
            spikes = self.get_click_points(detect_spike)

            for spike in spikes:
                spike_x, spike_y = spike

                # Distance from spike to ship
                sx = spike_x - self.ship_x
                sy = abs(self.ship_y - spike_y)

                if sy < 125:
                    if -15 <= sx <= 15:
                        if self.center:
                            move = randint(0, 1)
                            if move == 0:
                                self.kb.hold_left()
                                self.left = True
                            elif move == 1:
                                self.kb.hold_right()
                                self.right = True
                            self.center = False
                    elif sx < -20:
                        if self.left:
                            self.kb.center()
                            self.left = False
                            self.center = True
                    elif sx > 20:
                        if self.right:
                            self.kb.center()
                            self.right = False
                            self.center = True

    def hit_block(self, screenshot):
        detect_block = self.block_cascade.detectMultiScale(screenshot)

        if len(detect_block) > 0:
            blocks = self.get_click_points(detect_block)

            for block in blocks:
                block_x, block_y = block

                # Distance from block to ship
                bx = block_x - self.ship_x
                by = abs(self.ship_y - block_y)

                if by < 75:
                    if bx < -15:
                        if self.center:
                            self.kb.hold_left()
                            self.left = True
                            self.center = False
                        elif self.right:
                            self.kb.center()
                            self.right = False
                            self.center = True
                    elif bx > 15:
                        if self.center:
                            self.kb.hold_right()
                            self.right = True
                            self.center = False
                        elif self.left:
                            self.kb.center()
                            self.left = False
                            self.center = True
