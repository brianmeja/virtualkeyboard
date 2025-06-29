<<<<<<< HEAD
# Virtual Keyboard System

A touchless typing system that uses computer vision and hand tracking to simulate keyboard input.

## 🎯 Features

- **Virtual QWERTY Keyboard**: On-screen keyboard with visual feedback
- **Hand Tracking**: Real-time finger position detection using MediaPipe
- **Touchless Typing**: Type without physically touching a keyboard
- **Visual Feedback**: Key highlighting and animations
- **Responsive Performance**: 15+ FPS tracking and <100ms typing latency

## 🛠 Requirements

- Python 3.8+
- Webcam (720p or above recommended)
- Windows/macOS/Linux

## 📦 Installation

1. Clone this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 🚀 Usage

Run the main application:
```bash
python virtual_keyboard.py
```

### Controls
- **Index Finger**: Point to keys to type
- **ESC**: Exit the application
- **Space**: Toggle keyboard visibility

## 🎮 How It Works

1. **Hand Detection**: MediaPipe tracks your hand landmarks in real-time
2. **Finger Tracking**: Index fingertip (landmark 8) is tracked for key interaction
3. **Key Detection**: When your finger overlaps a virtual key, it highlights
4. **Typing Logic**: Press detection uses depth/movement logic to confirm intent
5. **Input Simulation**: Valid presses are converted to actual keystrokes

## 🔧 Configuration

Edit `config.py` to customize:
- Keyboard layout and positioning
- Tracking sensitivity
- Visual appearance
- Performance settings

## 📁 Project Structure

```
virtualkeyboard/
├── virtual_keyboard.py    # Main application
├── keyboard_layout.py     # Keyboard UI and layout
├── hand_tracker.py        # MediaPipe hand tracking
├── input_simulator.py     # Keystroke simulation
├── config.py             # Configuration settings
├── requirements.txt      # Dependencies
└── README.md            # This file
```

## 🎯 Performance Tips

- Ensure good lighting for hand tracking
- Keep hands within camera view
- Maintain 30-60cm distance from camera
- Use a solid background for better tracking

## 🔮 Future Enhancements

- Multi-language keyboard layouts
- Gesture controls (space, backspace, shift)
- Calibration wizard
- Typing analytics and training
- VR/AR integration

## 📝 License

MIT License - feel free to use and modify! 
=======
# virtualkeyboard
>>>>>>> origin/main
