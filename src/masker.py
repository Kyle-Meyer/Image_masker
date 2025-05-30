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
        self.initialize_mask()
        self.setup_sketcher()

    def load_image(self):
        #attempt to load in the image with the path given
        self.Isrc = cv2.imread(self.image_path, cv2.IMREAD_COLOR)

        if self.Isrc is None:
            raise ValueError("Error, could not load image from path ", self.image_path)

        print("loaded image: ", self.image_path)
        print("Image dims: ", self.Isrc.shape)
    
    def initialize_mask(self):
        height, width = self.Isrc.shape[:2]

        self.mask = np.zeros((height, width), dtype=np.uint8)

        self.display_image = self.Isrc.copy()

    def setup_sketcher(self):
        self.sketcher = Sketcher('Image Window', self.display_image, self.mask)

    #as the function is named, make the mask with two copies of the image 
    #one is gray scale to let us know what isnt masked 
    #the other is color so we know what is in the mask 
    def process_mask_and_display(self):
        #convert source image to gray scale
        gray = cv2.cvtColor(self.Isrc, cv2.COLOR_BGR2GRAY)

        #convert gray scale back to 3 channel color for blending
        gray_3channel = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)

        #create an inverse mask using bitwise_not
        inverse_mask = cv2.bitwise_not(self.mask)

        #apply masks using bitwise operations (AND)
        #masked area from original color image
        color_region = cv2.bitwise_and(self.Isrc, self.Isrc, maske = self.mask) 

        #unmasked area from grayscale image to let us know whats not being selected 
        gray_region = cv2.bitwise_and(gray_3channel, gray_3channel, mask = inverse_mask)

        #now we combine both regions to make the final image 
        self.Ioutput = cv2.bitwise_or(color_region, gray_region)

        #display result
        cv2.namedWindow('Output')
        cv2.imshow('Output', self.Ioutput)

    #utility function to clear the mask and display the image 
    def clear_mask(self):
        self.mask.fill(0)

        self.display_image = self.Isrc.copy()
        self.sketcher.img = self.display_image

        print("mask cleared")

    def save_output(self, output_path):
        if self.Ioutput is not None:
            cv2.imwrite(output_path, self.Ioutput)
        else:
            print("output path is None, cannot save")

    #nice utility to get some stats for print outs
    def get_mask_stats(self):
        total_pixels = self.mask.size 
        masked_pixels = cv2.countNonZero(self.mask)
        mask_percentage = (masked_pixels / total_pixels) * 100

        return {
                'total_pixels': total_pixels,
                'masked_pixels': masked_pixels,
                'mask_percentage': mask_percentage
        }

    # command to wrap all of our functions 
    def run(self):
        cv2.namedWindow('Image Window')
        #set the mouse callback
        cv2.setMouseCallback('Image Window', self.sketcher.onmouse)

        self.print_instructions()

        while True:
            cv2.imshow('Image Window', self.display_image)

            #wait for a key press! Other wise the window does NOTHING
            key = cv2.waitKey(30) & 0xFF #why is it like this

            # Handle key presses
            if key == ord('r') or key == ord('R'):
                self.process_mask_and_display()
                stats = self.get_mask_stats()
                print(f"Processed mask: {stats['mask_percentage']:.1f}% of image masked")
            
            elif key == ord('c') or key == ord('C'):
                self.clear_mask()
            
            elif key == ord('s') or key == ord('S'):
                if self.Ioutput is not None:
                    output_name = f"output_{os.path.splitext(os.path.basename(self.image_path))[0]}.jpg"
                    self.save_output(output_name)
                else:
                    print("No output to save. Press 'r' first to process the mask.")
            
            elif key == ord('i') or key == ord('I'):
                stats = self.get_mask_stats()
                print(f"Mask info: {stats['masked_pixels']} pixels masked ({stats['mask_percentage']:.1f}%)")
            
            elif key == self.ESC_KEY or key == ord('q'):
                break
        
        # Clean up
        cv2.destroyAllWindows()
        print("Program ended")
    
    def _print_instructions(self):
        """Print usage instructions to console."""
        print("\n" + "="*50)
        print("IMAGE MASKER INSTRUCTIONS:")
        print("="*50)
        print("- Draw on the image with left mouse button")
        print("- Press 'r' to process and show result")
        print("- Press 'c' to clear mask")
        print("- Press 's' to save output image")
        print("- Press 'i' to show mask info")
        print("- Press ESC or 'q' to quit")
        print("="*50 + "\n")


def main():
    """Main function to run the Image Masker application."""
    if len(sys.argv) != 2:
        print("Usage: python image_masker.py <image_path>")
        print("Example: python image_masker.py sample.jpg")
        return
    
    image_path = sys.argv[1]
    
    try:
        # Create ImageMasker instance
        masker = ImageMasker(image_path)
        
        # Run the application
        masker.run()
        
    except ValueError as e:
        print(e)
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()


