import cv2 
import numpy as np 


class sketcher:
    def __init__(self, window_name, display_image, mask, brush_size=10):
        self.window_name = window_name
        self.display_image = display_image
        self.mask = mask
        self.brush_size = brush_size

        self.drawing = False
        self.last_point=None 

        self.mask_color = 255
        self.display_color = (0,255,0)

    def mouse_callback(self, event, x, y, flags, param):
        current_point = (x, y)

        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.last_point = current_point 
            self.draw_at_point(x, y)

        elif event == cv2.EVENT_MOUSEMOVE and self.drawing:
            if self.last_point is None:
                self.draw_line(self.last_point, self.current_point)
            self.last_point = current_point

        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False 
            self.last_point = None 

    def draw_at_point(self, x, y):
        #cirlce on mask
        cv2.circle(self.mask, (x, y), self.brush_size, self.display_color, -1)
        #outline circle for visual feedback
        cv2.circle(self.display_image, (x,y), self.brush_size, self.display_color, 2)

    def draw_line(self, pt1, pt2):
        #line for the mask
        cv2.line(self.mask, pt1, pt2, self.mask_color, self.brush_size * 2)
        #line for the display image
        cv2.line(self.mask, pt1, pt2, self.display_color, 2)

    def set_brush_size(self, size):
        self.brush_size = max(1, min(50, size))

    def get_brush_size(self):
        return self.brush_size
    
    def clear_drawing(self):
        self.mask.fill(0)
        self.drawing = False 
        self.last_point = None

    def set_mask_color(self, color):
        self.mask_color = color 

    def set_display_color(self, color):
        self.display_color = color  

    def update_images(self, display_image, mask):
        self.display_image = display_image
        self.mask = mask
        self.drawing = False 
        self.last_point = None 
