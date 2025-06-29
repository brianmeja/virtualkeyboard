"""
Virtual Keyboard Main Application
"""

import cv2
import time
import numpy as np
from keyboard_layout import VirtualKeyboard
from hand_tracker import HandTracker
from input_simulator import InputSimulator
from config import *

class VirtualKeyboardApp:
    def __init__(self):
        self.keyboard = VirtualKeyboard()
        self.hand_tracker = HandTracker()
        self.input_simulator = InputSimulator()
        
        self.cap = None
        self.running = False
        self.show_keyboard = True
        self.fps_counter = 0
        self.fps_start_time = time.time()
        self.current_fps = 0
        
        # Typing state
        self.current_hover_key = None
        self.current_press_key = None
        self.last_landmarks = None
        
    def initialize_camera(self):
        """Initialize the webcam"""
        self.cap = cv2.VideoCapture(CAMERA_INDEX)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_WIDTH)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_HEIGHT)
        
        if not self.cap.isOpened():
            print("Error: Could not open camera")
            return False
        
        print("Camera initialized successfully")
        return True
    
    def process_typing_logic(self, landmarks):
        """Process the typing logic based on hand landmarks"""
        if not landmarks:
            self._clear_keyboard_states()
            return
        
        # Get the first hand (primary hand)
        primary_hand = landmarks[0]
        
        # Get finger tip position
        finger_tip = self.hand_tracker.get_index_finger_tip(primary_hand)
        if not finger_tip:
            self._clear_keyboard_states()
            return
        
        # Map camera coordinates to display coordinates
        display_x = int(finger_tip['x'] * DISPLAY_WIDTH / CAMERA_WIDTH)
        display_y = int(finger_tip['y'] * DISPLAY_HEIGHT / CAMERA_HEIGHT)
        
        # Check if finger is over a key
        key_id, key_data = self.keyboard.get_key_at_position(display_x, display_y)
        
        # Update hover state
        if key_id != self.current_hover_key:
            self.current_hover_key = key_id
            self.keyboard.set_hover_key(key_id)
        
        # Check if finger is pressed (close to palm)
        is_pressed = self.hand_tracker.is_finger_pressed(primary_hand)
        
        # Process press logic
        if is_pressed and key_id and key_id != self.current_press_key:
            # New key press detected
            self.current_press_key = key_id
            self.keyboard.set_pressed_key(key_id)
            
            # Get the key character and press it
            key_char = self.keyboard.get_key_character(key_id)
            if key_char:
                success = self.input_simulator.press_key(key_char)
                if success:
                    print(f"Successfully pressed: {key_char}")
        
        elif not is_pressed:
            # Finger released
            if self.current_press_key:
                self.keyboard.clear_pressed_key()
                self.current_press_key = None
        
        # Store landmarks for next frame
        self.last_landmarks = primary_hand
    
    def _clear_keyboard_states(self):
        """Clear all keyboard states when no hand is detected"""
        self.current_hover_key = None
        self.current_press_key = None
        self.keyboard.set_hover_key(None)
        self.keyboard.clear_pressed_key()
    
    def draw_debug_info(self, frame):
        """Draw debug information on the frame"""
        if not DEBUG_MODE:
            return
        
        # Draw FPS
        if SHOW_FPS:
            cv2.putText(frame, f"FPS: {self.current_fps:.1f}", 
                       (10, DISPLAY_HEIGHT - 30), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, COLORS['text_normal'], 2)
        
        # Draw instructions
        instructions = [
            "ESC: Exit",
            "Space: Toggle Keyboard",
            "Index finger: Point to keys",
            "Bring finger close to palm to press"
        ]
        
        for i, instruction in enumerate(instructions):
            y_pos = 90 + i * 25
            cv2.putText(frame, instruction, (10, y_pos), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS['text_normal'], 1)
    
    def update_fps(self):
        """Update FPS counter"""
        self.fps_counter += 1
        current_time = time.time()
        
        if current_time - self.fps_start_time >= 1.0:
            self.current_fps = self.fps_counter / (current_time - self.fps_start_time)
            self.fps_counter = 0
            self.fps_start_time = current_time
    
    def run(self):
        """Main application loop"""
        if not self.initialize_camera():
            return
        
        print("Virtual Keyboard started!")
        print("Press ESC to exit, Space to toggle keyboard visibility")
        
        self.running = True
        
        try:
            while self.running:
                # Read frame from camera
                ret, frame = self.cap.read()
                if not ret:
                    print("Error reading frame")
                    break
                
                # Create display frame
                display_frame = np.zeros((DISPLAY_HEIGHT, DISPLAY_WIDTH, 3), dtype=np.uint8)
                display_frame[:] = COLORS['background']
                
                # Process hand tracking
                landmarks_list = self.hand_tracker.process_frame(frame)
                
                # Draw hand information on camera frame
                if landmarks_list:
                    self.hand_tracker.draw_finger_info(frame, landmarks_list[0])
                
                # Process typing logic
                self.process_typing_logic(landmarks_list)
                
                # Draw virtual keyboard
                if self.show_keyboard:
                    self.keyboard.draw(display_frame)
                
                # Draw camera feed (scaled down)
                camera_display_width = 320
                camera_display_height = 240
                camera_x = DISPLAY_WIDTH - camera_display_width - 20
                camera_y = 20
                
                # Resize camera frame for display
                camera_frame_resized = cv2.resize(frame, (camera_display_width, camera_display_height))
                
                # Overlay camera frame on display
                display_frame[camera_y:camera_y + camera_display_height, 
                            camera_x:camera_x + camera_display_width] = camera_frame_resized
                
                # Draw debug information
                self.draw_debug_info(display_frame)
                
                # Update FPS
                self.update_fps()
                
                # Display the frame
                cv2.imshow('Virtual Keyboard', display_frame)
                
                # Handle key events
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC
                    break
                elif key == 32:  # Space
                    self.show_keyboard = not self.show_keyboard
                    print(f"Keyboard visibility: {'ON' if self.show_keyboard else 'OFF'}")
        
        except KeyboardInterrupt:
            print("Interrupted by user")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        print("Cleaning up...")
        
        if self.cap:
            self.cap.release()
        
        self.hand_tracker.release()
        self.input_simulator.cleanup()
        cv2.destroyAllWindows()
        
        print("Virtual Keyboard closed")

def main():
    """Main entry point"""
    app = VirtualKeyboardApp()
    app.run()

if __name__ == "__main__":
    main() 