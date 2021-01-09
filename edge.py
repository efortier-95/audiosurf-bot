

"""
Canny Edge: https://docs.opencv.org/master/da/d22/tutorial_py_canny.html
Erode and Dilate: https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_morphological_ops/py_morphological_ops.html
"""


# Data structure to hold state of Canny edge filter
class EdgeFilter:

    def __init__(self, kernelSize=None, erodeIter=None, dilateIter=None,
                 canny1=None, canny2=None):
        self.kernelSize = kernelSize
        self.erodeIter = erodeIter
        self.dilateIter = dilateIter
        self.canny1 = canny1
        self.canny2 = canny2
