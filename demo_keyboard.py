"""
Demo script to show the virtual keyboard layout
"""

import cv2
import numpy as np
from keyboard_layout import VirtualKeyboard
from config import *

def main():
    """Demo the virtual keyboard layout"""
    print("Virtual Keyboard Demo")
    print("Press any key to exit")
    
    # Create keyboard
    keyboard = VirtualKeyboard()
    
    # Create display window
    cv2.namedWindow('Virtual Keyboard Demo', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Virtual Keyboard Demo', DISPLAY_WIDTH, DISPLAY_HEIGHT)
    
    # Simulate mouse position
    mouse_x, mouse_y = DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2
    
    while True:
        # Create frame
        frame = np.zeros((DISPLAY_HEIGHT, DISPLAY_WIDTH, 3), dtype=np.uint8)
        frame[:] = COLORS['background']
        
        # Simulate mouse movement (circular motion)
        import math
        import time
        t = time.time()
        mouse_x = int(DISPLAY_WIDTH // 2 + 200 * math.cos(t))
        mouse_y = int(DISPLAY_HEIGHT // 2 + 100 * math.sin(t))
        
        # Get key under mouse
        key_id, key_data = keyboard.get_key_at_position(mouse_x, mouse_y)
        keyboard.set_hover_key(key_id)
        
        # Draw keyboard
        keyboard.draw(frame)
        
        # Draw mouse cursor
        cv2.circle(frame, (mouse_x, mouse_y), 5, (0, 255, 255), -1)
        cv2.circle(frame, (mouse_x, mouse_y), 8, (255, 255, 255), 2)
        
        # Draw info
        info_text = f"Mouse: ({mouse_x}, {mouse_y})"
        if key_id:
            key_char = keyboard.get_key_character(key_id)
            info_text += f" | Key: {key_char}"
        else:
            info_text += " | Key: None"
        
        cv2.putText(frame, info_text, (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLORS['text_normal'], 2)
        
        cv2.putText(frame, "Press any key to exit", (10, DISPLAY_HEIGHT - 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, COLORS['text_normal'], 2)
        
        # Show frame
        cv2.imshow('Virtual Keyboard Demo', frame)
        
        # Check for key press
        if cv2.waitKey(30) & 0xFF != 255:
            break
    
    cv2.destroyAllWindows()
    print("Demo finished")

if __name__ == "__main__":
    main() 