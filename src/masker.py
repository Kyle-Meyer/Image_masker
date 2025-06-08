#!/usr/bin/env python3

# Required imports
import cv2
import numpy as np
import sys
import os

# Import our custom Sketcher class
from sketcher import Sketcher

class ImageMasker:
    
    def __init__(self, image_path):
        # Instance variables
        self.image_path = image_path
        self.Isrc = None          # Original color image
        self.mask = None          # Binary mask for drawing
        self.Ioutput = None       # Final output image
        self.display_image = None # Working copy for display
        self.sketcher = None      # Sketcher instance
        
        # Constants
        self.ESC_KEY = 27
        self.ENTER_KEY = 13
        
        # Load and initialize the image
        self._load_image()
        self._initialize_mask()
        self._setup_sketcher()
    
    def _load_image(self):
        self.Isrc = cv2.imread(self.image_path, cv2.IMREAD_COLOR)
        
        if self.Isrc is None:
            raise ValueError(f"Error: Could not load image from {self.image_path}")
        
        print(f"Loaded image: {self.image_path}")
        print(f"Image dimensions: {self.Isrc.shape}")
    
    def _initialize_mask(self):
        # Get image dimensions
        height, width = self.Isrc.shape[:2]
        
        # Initialize mask (all zeros/black)
        self.mask = np.zeros((height, width), dtype=np.uint8)
        
        # Create a copy of source image for display
        self.display_image = self.Isrc.copy()
    
    def _setup_sketcher(self):
        # Pass references to our actual mask and display image
        self.sketcher = Sketcher('Image Window', self.display_image, self.mask)
    
    def process_mask_and_display(self):
        # Convert source image to grayscale
        Igray = cv2.cvtColor(self.Isrc, cv2.COLOR_BGR2GRAY)
        
        # Convert grayscale back to 3-channel for blending
        Igray_3channel = cv2.cvtColor(Igray, cv2.COLOR_GRAY2BGR)
        
        # Create inverse mask
        inverse_mask = cv2.bitwise_not(self.mask)
        
        # Apply masks using bitwise operations
        # Masked area from original color image
        color_region = cv2.bitwise_and(self.Isrc, self.Isrc, mask=self.mask)
        
        # Unmasked area from grayscale image
        gray_region = cv2.bitwise_and(Igray_3channel, Igray_3channel, mask=inverse_mask)
        
        # Combine both regions
        self.Ioutput = cv2.bitwise_or(color_region, gray_region)
        
        # Display result
        cv2.namedWindow('Output')
        cv2.imshow('Output', self.Ioutput)
    
    def clear_mask(self):
        """Clear the current mask and reset the display image."""
        # Reset display image to original
        self.display_image = self.Isrc.copy()
        
        # Clear the sketcher's drawing
        self.sketcher.clear_drawing()
        
        # Update sketcher with fresh images
        self.sketcher.update_images(self.display_image, self.mask)
        
        print("Mask cleared")
    
    def save_output(self, output_path):
        if self.Ioutput is not None:
            cv2.imwrite(output_path, self.Ioutput)
            print(f"Output saved to: {output_path}")
        else:
            print("No output image to save. Press 'r' first to process the mask.")
    
    def change_brush_size(self, delta):
        current_size = self.sketcher.get_brush_size()
        new_size = current_size + delta
        self.sketcher.set_brush_size(new_size)
        print(f"Brush size: {self.sketcher.get_brush_size()}")
    
    def get_mask_stats(self):
        total_pixels = self.mask.size
        masked_pixels = cv2.countNonZero(self.mask)
        mask_percentage = (masked_pixels / total_pixels) * 100
        
        return {
            'total_pixels': total_pixels,
            'masked_pixels': masked_pixels,
            'mask_percentage': mask_percentage
        }
    
    def run(self):
        # Create window and set mouse callback
        cv2.namedWindow('Image Window')
        cv2.setMouseCallback('Image Window', self.sketcher.mouse_callback)
        
        # Print instructions
        self._print_instructions()
        
        # Main program loop
        while True:
            # Animate marching ants
            self.sketcher.animate_ants()
            self.sketcher.update_display()
            # Display the sketcher's image because its handling color corrections
            cv2.imshow('Image Window', self.sketcher.display_image)
            
            # Wait for key press
            key = cv2.waitKey(30) & 0xFF
            
            # Handle key presses
            if key == ord('r') or key == ord('R'):
                # Debug: Check if mask has any white pixels
                masked_pixels = cv2.countNonZero(self.mask)
                print(f"Debug: Mask has {masked_pixels} white pixels before processing")
                
                if masked_pixels > 0:
                    self.process_mask_and_display()
                    stats = self.get_mask_stats()
                    print(f"Processed mask: {stats['mask_percentage']:.1f}% of image masked")
                else:
                    print("No mask drawn yet. Draw on the image first, then press 'r'.")
            
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
            
            elif key == ord('+') or key == ord('='):
                self.change_brush_size(2)
            
            elif key == ord('-') or key == ord('_'):
                self.change_brush_size(-2)
            
            elif key == ord('m') or key == ord('M'):
                # Show mask as black and white image
                masked_pixels = cv2.countNonZero(self.mask)
                print(f"Debug: Mask has {masked_pixels} white pixels")
                cv2.namedWindow('Mask View')
                cv2.imshow('Mask View', self.mask)
            
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
        print("- Press 'm' to view mask")
        print("- Press '+'/'-' to increase/decrease brush size")
        print("- Press ESC or 'q' to quit")
        print("="*50 + "\n")


def main():
    """Main function to run the Image Masker application."""
    if len(sys.argv) != 2:
        print("Usage: python masker.py <image_path>")
        print("Example: python masker.py sample.jpg")
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



