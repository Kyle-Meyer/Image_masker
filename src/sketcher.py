#!/usr/bin/env python3

import cv2
import numpy as np

class Sketcher:
    """
    A class to handle interactive drawing on images.
    Allows users to draw masks using mouse input.
    """
    
    def __init__(self, window_name, display_image, mask, brush_size=10):
        self.window_name = window_name
        self.display_image = display_image.copy() #python only works in shallow copies by default!
        self.original_image = display_image.copy()
        self.mask = mask
        self.brush_size = brush_size
        
        # Drawing state
        self.drawing = False
        self.last_point = None
        
        # Colors
        self.mask_color = 255  # White for mask
        self.display_color = (0, 255, 0)  # Green for visual feedback
    
    def mouse_callback(self, event, x, y, flags, param):
        current_point = (x, y)
        
        if event == cv2.EVENT_LBUTTONDOWN:
            # Start drawing
            self.drawing = True
            self.last_point = current_point
            self.draw_at_point(x, y)
        
        elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
            # Continue drawing - draw line from last point to current point
            if self.last_point is not None:
                self.draw_line(self.last_point, current_point)
            self.last_point = current_point
        
        elif event == cv2.EVENT_LBUTTONUP:
            # Stop drawing
            self.drawing = False
            self.last_point = None
    
    def draw_at_point(self, x, y):
        # Debug print
        print(f"Drawing at point ({x}, {y}) with brush size {self.brush_size}")
        
        # Draw filled circle on mask
        cv2.circle(self.mask, (x, y), self.brush_size, self.mask_color, -1)
        
        # Update display to show inverted colors where mask is white
        self.update_display()
        
        masked_pixels = cv2.countNonZero(self.mask)
        print(f"Debug: Mask now has {masked_pixels} white pixels")
    

    def draw_line(self, pt1, pt2):
        distance = int(np.sqrt((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2))
        
        if distance == 0:
            self.draw_at_point(pt2[0], pt2[1])
            return
        
        num_steps = max(distance // (self.brush_size // 3), 1)
        
        for i in range(num_steps + 1):
            t = i / num_steps if num_steps > 0 else 0
            x = int(pt1[0] + t * (pt2[0] - pt1[0]))
            y = int(pt1[1] + t * (pt2[1] - pt1[1]))
            
            # Draw filled circle on mask
            cv2.circle(self.mask, (x, y), self.brush_size, self.mask_color, -1)
        
        # Update display once after drawing the entire line
        self.update_display()

    def update_display(self):
        # Reset display to original
        self.display_image = self.original_image.copy()
        
        # Apply inversion only where mask is white
        mask_bool = self.mask == 255
        self.display_image[mask_bool] = 255 - self.display_image[mask_bool]

    def set_brush_size(self, size):
        self.brush_size = max(1, min(50, size))
    
    def get_brush_size(self):
        return self.brush_size
    
    def clear_drawing(self):
        self.mask.fill(0)
        self.drawing = False
        self.last_point = None
        # Update display after clearing
        self.update_display()
    
    def set_mask_color(self, color):
        self.mask_color = color
    
    def set_display_color(self, color):
        self.display_color = color
    
    def update_images(self, display_image, mask):
        self.display_image = display_image
        self.original_image = display_image.copy()  
        self.mask = mask
        self.drawing = False
        self.last_point = None
        # Update display with new images
        self.update_display()
