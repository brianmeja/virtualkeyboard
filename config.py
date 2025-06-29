"""
Configuration settings for the Virtual Keyboard System
"""

# Display Settings
DISPLAY_WIDTH = 1280
DISPLAY_HEIGHT = 720
FPS_TARGET = 30

# Keyboard Layout Settings
KEYBOARD_WIDTH = 1000
KEYBOARD_HEIGHT = 300
KEYBOARD_X = (DISPLAY_WIDTH - KEYBOARD_WIDTH) // 2
KEYBOARD_Y = DISPLAY_HEIGHT - KEYBOARD_HEIGHT - 50

# Key Dimensions
KEY_WIDTH = 60
KEY_HEIGHT = 60
KEY_SPACING = 5
KEY_ROUNDING = 8

# Colors (BGR format for OpenCV)
COLORS = {
    'background': (40, 40, 40),
    'key_normal': (60, 60, 60),
    'key_hover': (80, 120, 200),
    'key_pressed': (120, 80, 200),
    'text_normal': (200, 200, 200),
    'text_hover': (255, 255, 255),
    'hand_landmarks': (0, 255, 0),
    'finger_tip': (0, 255, 255),
    'palm_center': (255, 0, 0)
}

# Hand Tracking Settings
HAND_CONFIDENCE = 0.7
MAX_NUM_HANDS = 2
INDEX_FINGER_TIP_ID = 8
PALM_CENTER_ID = 0

# Typing Logic Settings
PRESS_THRESHOLD_DISTANCE = 40  # pixels from palm center
DEBOUNCE_TIME = 0.3  # seconds between valid presses
MOVEMENT_THRESHOLD = 10  # minimum movement to confirm press

# Camera Settings
CAMERA_INDEX = 0
CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480

# Performance Settings
SKIP_FRAMES = 1  # Process every Nth frame for performance
BLUR_KERNEL = (5, 5)  # Gaussian blur for noise reduction

# QWERTY Keyboard Layout
KEYBOARD_LAYOUT = [
    ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'backspace'],
    ['tab', 'q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
    ['caps', 'a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', "'", 'enter'],
    ['shift', 'z', 'x', 'c', 'v', 'b', 'n', 'm', ',', '.', '/', 'shift'],
    ['ctrl', 'win', 'alt', 'space', 'alt', 'win', 'menu', 'ctrl']
]

# Special key mappings
SPECIAL_KEYS = {
    'backspace': 'backspace',
    'tab': 'tab',
    'caps': 'capslock',
    'enter': 'enter',
    'shift': 'shift',
    'ctrl': 'ctrl',
    'alt': 'alt',
    'win': 'win',
    'space': 'space',
    'menu': 'menu'
}

# Debug Settings
DEBUG_MODE = True
SHOW_FPS = True
SHOW_LANDMARKS = True
SHOW_BOUNDING_BOXES = True
SHOW_DISTANCE_LINES = True 