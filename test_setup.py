"""
Test script to verify Virtual Keyboard setup
"""

import sys
import importlib

def test_imports():
    """Test if all required modules can be imported"""
    required_modules = [
        'cv2',
        'mediapipe',
        'pyautogui',
        'keyboard',
        'numpy'
    ]
    
    print("Testing module imports...")
    failed_imports = []
    
    for module in required_modules:
        try:
            importlib.import_module(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\nFailed to import: {', '.join(failed_imports)}")
        print("Please install missing dependencies with: pip install -r requirements.txt")
        return False
    
    print("All modules imported successfully!")
    return True

def test_camera():
    """Test if camera can be accessed"""
    try:
        import cv2
        cap = cv2.VideoCapture(0)
        if cap.isOpened():
            ret, frame = cap.read()
            cap.release()
            if ret:
                print("✓ Camera access successful")
                return True
            else:
                print("✗ Camera access failed: Could not read frame")
                return False
        else:
            print("✗ Camera access failed: Could not open camera")
            return False
    except Exception as e:
        print(f"✗ Camera test failed: {e}")
        return False

def test_mediapipe():
    """Test MediaPipe hand tracking"""
    try:
        import mediapipe as mp
        import cv2
        import numpy as np
        
        # Create a test frame
        test_frame = np.zeros((480, 640, 3), dtype=np.uint8)
        
        # Initialize MediaPipe
        mp_hands = mp.solutions.hands
        hands = mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.7
        )
        
        # Process test frame
        rgb_frame = cv2.cvtColor(test_frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        
        hands.close()
        print("✓ MediaPipe hand tracking initialized successfully")
        return True
        
    except Exception as e:
        print(f"✗ MediaPipe test failed: {e}")
        return False

def test_local_modules():
    """Test if local modules can be imported"""
    local_modules = [
        'config',
        'keyboard_layout',
        'hand_tracker',
        'input_simulator',
        'virtual_keyboard'
    ]
    
    print("\nTesting local module imports...")
    failed_imports = []
    
    for module in local_modules:
        try:
            importlib.import_module(module)
            print(f"✓ {module}")
        except ImportError as e:
            print(f"✗ {module}: {e}")
            failed_imports.append(module)
    
    if failed_imports:
        print(f"\nFailed to import local modules: {', '.join(failed_imports)}")
        return False
    
    print("All local modules imported successfully!")
    return True

def main():
    """Run all tests"""
    print("Virtual Keyboard Setup Test")
    print("=" * 40)
    
    # Test external dependencies
    if not test_imports():
        return False
    
    # Test camera
    if not test_camera():
        print("\nWarning: Camera test failed. The virtual keyboard may not work properly.")
    
    # Test MediaPipe
    if not test_mediapipe():
        return False
    
    # Test local modules
    if not test_local_modules():
        return False
    
    print("\n" + "=" * 40)
    print("✓ All tests passed! Virtual Keyboard is ready to use.")
    print("\nTo start the virtual keyboard, run:")
    print("python virtual_keyboard.py")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 