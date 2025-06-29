"""
Virtual Keyboard Layout and UI Management
"""

import cv2
import numpy as np
from config import *

class VirtualKeyboard:
    def __init__(self):
        self.keys = {}
        self.pressed_key = None
        self.hover_key = None
        self._build_keyboard()
    
    def _build_keyboard(self):
        """Build the keyboard layout with key positions"""
        current_y = KEYBOARD_Y
        
        for row_idx, row in enumerate(KEYBOARD_LAYOUT):
            # Calculate row width to center it
            row_width = len(row) * (KEY_WIDTH + KEY_SPACING) - KEY_SPACING
            current_x = KEYBOARD_X + (KEYBOARD_WIDTH - row_width) // 2
            
            for col_idx, key_char in enumerate(row):
                # Adjust key width for special keys
                key_w = KEY_WIDTH
                if key_char in ['backspace', 'tab', 'caps', 'enter', 'shift', 'space']:
                    if key_char == 'space':
                        key_w = KEY_WIDTH * 6
                    elif key_char in ['backspace', 'enter']:
                        key_w = KEY_WIDTH * 1.5
                    elif key_char in ['tab', 'caps', 'shift']:
                        key_w = KEY_WIDTH * 1.3
                
                # Create key bounding box
                key_rect = {
                    'x': int(current_x),
                    'y': int(current_y),
                    'width': int(key_w),
                    'height': KEY_HEIGHT,
                    'char': key_char,
                    'row': row_idx,
                    'col': col_idx
                }
                
                self.keys[f"{row_idx}_{col_idx}"] = key_rect
                current_x += key_w + KEY_SPACING
            
            current_y += KEY_HEIGHT + KEY_SPACING
    
    def get_key_at_position(self, x, y):
        """Get the key at the given screen position"""
        for key_id, key in self.keys.items():
            if (key['x'] <= x <= key['x'] + key['width'] and 
                key['y'] <= y <= key['y'] + key['height']):
                return key_id, key
        return None, None
    
    def set_hover_key(self, key_id):
        """Set the currently hovered key"""
        self.hover_key = key_id
    
    def set_pressed_key(self, key_id):
        """Set the currently pressed key"""
        self.pressed_key = key_id
    
    def clear_pressed_key(self):
        """Clear the pressed key state"""
        self.pressed_key = None
    
    def draw(self, frame):
        """Draw the virtual keyboard on the frame"""
        # Draw background rectangle for keyboard
        cv2.rectangle(frame, 
                     (KEYBOARD_X, KEYBOARD_Y), 
                     (KEYBOARD_X + KEYBOARD_WIDTH, KEYBOARD_Y + KEYBOARD_HEIGHT),
                     COLORS['background'], -1)
        
        # Draw each key
        for key_id, key in self.keys.items():
            # Determine key color based on state
            if key_id == self.pressed_key:
                color = COLORS['key_pressed']
                text_color = COLORS['text_hover']
            elif key_id == self.hover_key:
                color = COLORS['key_hover']
                text_color = COLORS['text_hover']
            else:
                color = COLORS['key_normal']
                text_color = COLORS['text_normal']
            
            # Draw key rectangle with rounded corners
            self._draw_rounded_rect(frame, 
                                  (key['x'], key['y']), 
                                  (key['x'] + key['width'], key['y'] + key['height']),
                                  color, KEY_ROUNDING)
            
            # Draw key text
            text = key['char'].upper() if len(key['char']) == 1 else key['char']
            text_size = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)[0]
            text_x = key['x'] + (key['width'] - text_size[0]) // 2
            text_y = key['y'] + (key['height'] + text_size[1]) // 2
            
            cv2.putText(frame, text, (text_x, text_y), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, text_color, 2)
            
            # Draw bounding box in debug mode
            if DEBUG_MODE and SHOW_BOUNDING_BOXES:
                cv2.rectangle(frame, 
                             (key['x'], key['y']), 
                             (key['x'] + key['width'], key['y'] + key['height']),
                             (255, 255, 0), 1)
    
    def _draw_rounded_rect(self, frame, top_left, bottom_right, color, radius):
        """Draw a rectangle with rounded corners"""
        x1, y1 = top_left
        x2, y2 = bottom_right
        
        # Draw main rectangle
        cv2.rectangle(frame, (x1 + radius, y1), (x2 - radius, y2), color, -1)
        cv2.rectangle(frame, (x1, y1 + radius), (x2, y2 - radius), color, -1)
        
        # Draw corner circles
        cv2.circle(frame, (x1 + radius, y1 + radius), radius, color, -1)
        cv2.circle(frame, (x2 - radius, y1 + radius), radius, color, -1)
        cv2.circle(frame, (x1 + radius, y2 - radius), radius, color, -1)
        cv2.circle(frame, (x2 - radius, y2 - radius), radius, color, -1)
    
    def get_key_character(self, key_id):
        """Get the character or special key for a given key ID"""
        if key_id in self.keys:
            return self.keys[key_id]['char']
        return None
    
    def is_special_key(self, key_char):
        """Check if a key character is a special key"""
        return key_char in SPECIAL_KEYS
    
    def get_special_key_name(self, key_char):
        """Get the special key name for simulation"""
        return SPECIAL_KEYS.get(key_char, key_char) 