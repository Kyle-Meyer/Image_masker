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
        self.current_mouse_pos = None
        
        # Colors
        self.mask_color = 255  # White for mask
        self.display_color = (0, 255, 0)  # Green for visual feedback
        
        # Marching ants animation
        self.ant_offset = 0
    
    def mouse_callback(self, event, x, y, flags, param):
        current_point = (x, y)
        self.current_mouse_pos = current_point
        
        if event == cv2.EVENT_LBUTTONDOWN:
            # Start drawing
            self.drawing = True
            self.last_point = current_point
            self.draw_at_point(x, y)
        
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                # Continue drawing - draw line from last point to current point
                if self.last_point is not None:
                    self.draw_line(self.last_point, current_point)
                self.last_point = current_point
        
        elif event == cv2.EVENT_LBUTTONUP:
            # Stop drawing
            self.drawing = False
            self.last_point = None
    
    def draw_at_point(self, x, y):
        # Draw filled circle on mask
        cv2.circle(self.mask, (x, y), self.brush_size, self.mask_color, -1)
        
        # Update display to show inverted colors where mask is white
        self.update_display()
    
    def draw_line(self, pt1, pt2):
        distance = int(np.sqrt((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2))
        
        if distance == 0:
            self.draw_at_point(pt2[0], pt2[1])
            return
        
        step_size = max(self.brush_size // 3, 1)  # prevent divide by 0
        num_steps = max(distance // step_size, 1)
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
        
        # Add marching ants around masked areas
        self.draw_marching_ants()
        
        # Draw brush cursor
        self.draw_brush_cursor()
    
    def draw_marching_ants(self):
        """Draw simple marching ants around mask contours"""
        if cv2.countNonZero(self.mask) == 0:
            return
            
        # Find contours
        contours, _ = cv2.findContours(self.mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Draw animated dashed outline
        for contour in contours:
            if len(contour) < 3:
                continue
                
            # Draw the contour with dashed pattern
            self.draw_dashed_outline(contour)
    
    def draw_dashed_outline(self, contour):
        """Draw a proper dashed outline around contour"""
        contour = contour.reshape(-1, 2)
        
        # Parameters for marching ants
        dash_length = 8
        gap_length = 4
        total_pattern = dash_length + gap_length
        
        # Calculate total perimeter to properly distribute dashes
        total_perimeter = cv2.arcLength(contour.reshape(-1, 1, 2), True)
        
        current_length = 0
        
        for i in range(len(contour)):
            pt1 = tuple(contour[i])
            pt2 = tuple(contour[(i + 1) % len(contour)])
            
            # Calculate segment length
            segment_length = np.sqrt((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2)
            
            if segment_length < 1:
                continue
            
            # Draw dashed line segment
            self.draw_dashed_line(pt1, pt2, current_length, dash_length, gap_length, total_pattern)
            current_length += segment_length
    
    def draw_dashed_line(self, pt1, pt2, start_offset, dash_len, gap_len, pattern_len):
        """Draw a dashed line between two points"""
        # Calculate line parameters
        dx = pt2[0] - pt1[0]
        dy = pt2[1] - pt1[1]
        length = np.sqrt(dx*dx + dy*dy)
        
        if length == 0:
            return
            
        # Normalize direction
        dx_norm = dx / length
        dy_norm = dy / length
        
        # Current position along the line
        current_pos = 0
        
        while current_pos < length:
            # Calculate position in pattern (with animation offset)
            pattern_pos = (start_offset + current_pos + self.ant_offset) % pattern_len
            
            # Determine if we're in a dash or gap
            in_dash = pattern_pos < dash_len
            
            if in_dash:
                # Calculate end of current dash
                dash_end = min(current_pos + (dash_len - (pattern_pos % dash_len)), length)
                
                # Draw the dash segment
                start_x = int(pt1[0] + current_pos * dx_norm)
                start_y = int(pt1[1] + current_pos * dy_norm)
                end_x = int(pt1[0] + dash_end * dx_norm)
                end_y = int(pt1[1] + dash_end * dy_norm)
                
                # Alternate colors for better visibility
                color = (255, 255, 255) if int(pattern_pos / 2) % 2 == 0 else (0, 0, 0)
                cv2.line(self.display_image, (start_x, start_y), (end_x, end_y), color, 1)
                
                current_pos = dash_end
            else:
                # Skip gap
                gap_end = min(current_pos + (gap_len - ((pattern_pos - dash_len) % gap_len)), length)
                current_pos = gap_end
    
    def draw_brush_cursor(self):
        """Draw brush cursor at current mouse position"""
        if self.current_mouse_pos is None:
            return
            
        center = self.current_mouse_pos
        
        # Draw brush outline circle
        cv2.circle(self.display_image, center, self.brush_size, (255, 255, 255), 1)
        cv2.circle(self.display_image, center, self.brush_size, (0, 0, 0), 1)
        
        # Draw center crosshair
        cv2.line(self.display_image, 
                (center[0] - 5, center[1]), 
                (center[0] + 5, center[1]), 
                (255, 255, 255), 1)
        cv2.line(self.display_image, 
                (center[0], center[1] - 5), 
                (center[0], center[1] + 5), 
                (255, 255, 255), 1)
    
    def animate_ants(self):
        """Update marching ants animation"""
        self.ant_offset = (self.ant_offset + 0.5) % 12  # Slower, smoother animation

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
