"""
Hand Tracking using MediaPipe
"""

import cv2
import mediapipe as mp
import numpy as np
from config import *

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=MAX_NUM_HANDS,
            min_detection_confidence=HAND_CONFIDENCE,
            min_tracking_confidence=HAND_CONFIDENCE
        )
        
        self.previous_landmarks = None
        self.finger_positions = []
    
    def process_frame(self, frame):
        """Process a frame and return hand landmarks"""
        # Convert BGR to RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Process the frame
        results = self.hands.process(rgb_frame)
        
        landmarks_list = []
        
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                landmarks = self._extract_landmarks(hand_landmarks, frame.shape)
                landmarks_list.append(landmarks)
                
                # Draw landmarks if debug mode is enabled
                if DEBUG_MODE and SHOW_LANDMARKS:
                    self._draw_landmarks(frame, hand_landmarks)
        
        return landmarks_list
    
    def _extract_landmarks(self, hand_landmarks, frame_shape):
        """Extract landmark coordinates from MediaPipe results"""
        height, width, _ = frame_shape
        landmarks = {}
        
        for idx, landmark in enumerate(hand_landmarks.landmark):
            x = int(landmark.x * width)
            y = int(landmark.y * height)
            z = landmark.z
            
            landmarks[idx] = {
                'x': x,
                'y': y,
                'z': z,
                'relative_x': landmark.x,
                'relative_y': landmark.y,
                'relative_z': landmark.z
            }
        
        return landmarks
    
    def _draw_landmarks(self, frame, hand_landmarks):
        """Draw hand landmarks on the frame"""
        self.mp_drawing.draw_landmarks(
            frame,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_drawing_styles.get_default_hand_landmarks_style(),
            self.mp_drawing_styles.get_default_hand_connections_style()
        )
    
    def get_index_finger_tip(self, landmarks):
        """Get the index finger tip position"""
        if landmarks and INDEX_FINGER_TIP_ID in landmarks:
            return landmarks[INDEX_FINGER_TIP_ID]
        return None
    
    def get_palm_center(self, landmarks):
        """Get the palm center position"""
        if landmarks and PALM_CENTER_ID in landmarks:
            return landmarks[PALM_CENTER_ID]
        return None
    
    def calculate_finger_distance(self, landmarks):
        """Calculate distance between index finger tip and palm center"""
        finger_tip = self.get_index_finger_tip(landmarks)
        palm_center = self.get_palm_center(landmarks)
        
        if finger_tip and palm_center:
            distance = np.sqrt(
                (finger_tip['x'] - palm_center['x'])**2 + 
                (finger_tip['y'] - palm_center['y'])**2
            )
            return distance
        return None
    
    def is_finger_pressed(self, landmarks, threshold_distance=PRESS_THRESHOLD_DISTANCE):
        """Check if the finger is in a pressed position"""
        distance = self.calculate_finger_distance(landmarks)
        if distance is not None:
            return distance < threshold_distance
        return False
    
    def get_finger_movement(self, current_landmarks, previous_landmarks):
        """Calculate finger movement between frames"""
        if not current_landmarks or not previous_landmarks:
            return 0
        
        current_tip = self.get_index_finger_tip(current_landmarks)
        previous_tip = self.get_index_finger_tip(previous_landmarks)
        
        if current_tip and previous_tip:
            movement = np.sqrt(
                (current_tip['x'] - previous_tip['x'])**2 + 
                (current_tip['y'] - previous_tip['y'])**2
            )
            return movement
        return 0
    
    def draw_finger_info(self, frame, landmarks):
        """Draw finger position and distance information"""
        if not landmarks:
            return
        
        finger_tip = self.get_index_finger_tip(landmarks)
        palm_center = self.get_palm_center(landmarks)
        
        if finger_tip and palm_center:
            # Draw finger tip
            cv2.circle(frame, (finger_tip['x'], finger_tip['y']), 8, COLORS['finger_tip'], -1)
            
            # Draw palm center
            cv2.circle(frame, (palm_center['x'], palm_center['y']), 6, COLORS['palm_center'], -1)
            
            # Draw distance line
            if DEBUG_MODE and SHOW_DISTANCE_LINES:
                cv2.line(frame, 
                        (finger_tip['x'], finger_tip['y']), 
                        (palm_center['x'], palm_center['y']), 
                        COLORS['hand_landmarks'], 2)
            
            # Show distance text
            distance = self.calculate_finger_distance(landmarks)
            if distance is not None:
                cv2.putText(frame, f"Dist: {distance:.1f}px", 
                           (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, 
                           COLORS['text_normal'], 2)
                
                # Show press status
                is_pressed = self.is_finger_pressed(landmarks)
                status = "PRESSED" if is_pressed else "HOVER"
                color = COLORS['key_pressed'] if is_pressed else COLORS['key_hover']
                cv2.putText(frame, status, (10, 60), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
    
    def release(self):
        """Release MediaPipe resources"""
        self.hands.close() 