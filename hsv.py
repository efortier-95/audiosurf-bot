

"""
HSV Thresholding: https://docs.opencv.org/3.4/da/d97/tutorial_threshold_inRange.html
"""


# Data structure to hold state of HSV filter
class HSVFilter:

    def __init__(self, hMin=None, sMin=None, vMin=None, hMax=None, sMax=None, vMax=None,
                 sAdd=None, sSub=None, vAdd=None, vSub=None):
        self.hMin = hMin
        self.sMin = sMin
        self.vMin = vMin
        self.hMax = hMax
        self.sMax = sMax
        self.vMax = vMax
        self.sAdd = sAdd
        self.sSub = sSub
        self.vAdd = vAdd
        self.vSub = vSub
