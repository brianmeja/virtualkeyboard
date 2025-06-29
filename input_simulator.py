"""
Input Simulation for Virtual Keyboard
"""

import pyautogui
import keyboard
import time
from config import *

class InputSimulator:
    def __init__(self):
        self.last_press_time = 0
        self.debounce_time = DEBOUNCE_TIME
        self.pressed_keys = set()
        
        # Configure pyautogui for safety
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.01  # Small delay between actions
    
    def can_press_key(self):
        """Check if enough time has passed since last key press"""
        current_time = time.time()
        return current_time - self.last_press_time >= self.debounce_time
    
    def press_key(self, key_char):
        """Simulate a key press"""
        if not self.can_press_key():
            return False
        
        try:
            if self.is_special_key(key_char):
                self._press_special_key(key_char)
            else:
                self._press_character_key(key_char)
            
            self.last_press_time = time.time()
            return True
            
        except Exception as e:
            print(f"Error pressing key '{key_char}': {e}")
            return False
    
    def is_special_key(self, key_char):
        """Check if the key is a special key"""
        return key_char in SPECIAL_KEYS
    
    def _press_character_key(self, key_char):
        """Press a character key"""
        # Use pyautogui for character keys
        pyautogui.press(key_char)
        print(f"Pressed character: {key_char}")
    
    def _press_special_key(self, key_char):
        """Press a special key"""
        special_key_name = SPECIAL_KEYS.get(key_char, key_char)
        
        # Use keyboard library for special keys
        keyboard.press_and_release(special_key_name)
        print(f"Pressed special key: {key_char} -> {special_key_name}")
    
    def hold_key(self, key_char):
        """Hold down a key"""
        if key_char not in self.pressed_keys:
            try:
                if self.is_special_key(key_char):
                    special_key_name = SPECIAL_KEYS.get(key_char, key_char)
                    keyboard.press(special_key_name)
                else:
                    pyautogui.keyDown(key_char)
                
                self.pressed_keys.add(key_char)
                print(f"Holding key: {key_char}")
                
            except Exception as e:
                print(f"Error holding key '{key_char}': {e}")
    
    def release_key(self, key_char):
        """Release a held key"""
        if key_char in self.pressed_keys:
            try:
                if self.is_special_key(key_char):
                    special_key_name = SPECIAL_KEYS.get(key_char, key_char)
                    keyboard.release(special_key_name)
                else:
                    pyautogui.keyUp(key_char)
                
                self.pressed_keys.remove(key_char)
                print(f"Released key: {key_char}")
                
            except Exception as e:
                print(f"Error releasing key '{key_char}': {e}")
    
    def release_all_keys(self):
        """Release all currently held keys"""
        for key_char in list(self.pressed_keys):
            self.release_key(key_char)
    
    def type_text(self, text):
        """Type a string of text"""
        try:
            pyautogui.write(text)
            print(f"Typed text: {text}")
        except Exception as e:
            print(f"Error typing text '{text}': {e}")
    
    def get_key_info(self, key_char):
        """Get information about a key"""
        if self.is_special_key(key_char):
            return {
                'type': 'special',
                'name': SPECIAL_KEYS.get(key_char, key_char),
                'char': key_char
            }
        else:
            return {
                'type': 'character',
                'name': key_char,
                'char': key_char
            }
    
    def cleanup(self):
        """Clean up resources and release any held keys"""
        self.release_all_keys() 