#!/usr/bin/env python3

# Required imports
import cv2
import numpy as np
import sys
import os

# If you copied common.py to your project folder
from common import Sketcher

# Alternative: If you copied just the Sketcher class into your file
# (then you don't need the above import)

# Global variable declarations
Isrc = None          # Original color image
mask = None          # Binary mask for drawing
Ioutput = None       # Final output image
display_image = None # Working copy for display

class ImageMasker:
    """
    a class to handle selective image masking
    """
    
    def __init__(self, image_path):
        self.image_path = image_path
        self.Isrc = None # original color of the image
        self.mask = None
        self.Ioutput = None 
        self.disply_image = None 
        self.sketcher = None 

        self.ESC_KEY = 27 
        self.ENTER_KEY = 13

        self.load_image()
        #self.initialize_mask()
        #self.setup_sketcher()

    def load_image(self):
        #attempt to load in the image with the path given
        self.Isrc = cv2.imread(self.image_path, cv2.IMREAD_COLOR)

        if self.Isrc is None:
            raise ValueError("Error, could not load image from path ", self.image_path)

        print("loaded image: ", self.image_path)
        print("Image dims: ", self.Isrc.shape)




