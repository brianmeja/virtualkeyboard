# Virtual Keyboard Installation Guide

## Prerequisites

### 1. Python Installation
The Virtual Keyboard requires Python 3.8 or higher.

**Windows:**
- Download Python from [python.org](https://www.python.org/downloads/)
- During installation, make sure to check "Add Python to PATH"
- Or install from Microsoft Store: `winget install Python.Python.3.11`

**macOS:**
```bash
brew install python
```

**Linux:**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### 2. Verify Python Installation
```bash
python --version
# or
python3 --version
```

## Installation Steps

### 1. Clone or Download the Project
```bash
git clone <repository-url>
cd virtualkeyboard
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
# or
python -m pip install -r requirements.txt
```

### 3. Test the Setup
```bash
python test_setup.py
```

## Troubleshooting

### Common Issues

#### 1. Python not found
**Error:** `Python was not found; run without arguments to install from the Microsoft Store`

**Solution:**
- Install Python from [python.org](https://www.python.org/downloads/)
- Make sure to check "Add Python to PATH" during installation
- Restart your terminal/command prompt after installation

#### 2. Module import errors
**Error:** `ModuleNotFoundError: No module named 'cv2'`

**Solution:**
```bash
pip install opencv-python
pip install -r requirements.txt
```

#### 3. Camera access issues
**Error:** `Could not open camera`

**Solution:**
- Make sure your webcam is connected and working
- Check if other applications can access the camera
- Try changing `CAMERA_INDEX` in `config.py` (try 0, 1, 2, etc.)

#### 4. MediaPipe installation issues
**Error:** `Failed to import mediapipe`

**Solution:**
```bash
pip uninstall mediapipe
pip install mediapipe
```

### Windows-Specific Issues

#### 1. Microsoft Store Python
If you installed Python from Microsoft Store, you might need to:
```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

#### 2. Permission Issues
Run PowerShell as Administrator and try:
```powershell
Set-ExecutionPolicy RemoteSigned
```

### macOS-Specific Issues

#### 1. Camera permissions
Make sure to grant camera permissions to Terminal/iTerm in System Preferences > Security & Privacy > Privacy > Camera

#### 2. OpenCV issues
```bash
brew install opencv
pip install opencv-python
```

### Linux-Specific Issues

#### 1. Camera access
```bash
sudo apt install v4l-utils
v4l2-ctl --list-devices
```

#### 2. OpenCV dependencies
```bash
sudo apt install libopencv-dev python3-opencv
```

## Testing Your Installation

### 1. Run the test script
```bash
python test_setup.py
```

### 2. Try the demo (no camera required)
```bash
python demo_keyboard.py
```

### 3. Run the full application
```bash
python virtual_keyboard.py
```

## Usage Instructions

### Starting the Virtual Keyboard
1. Run `python virtual_keyboard.py`
2. Position your hand in front of the camera
3. Point your index finger at the virtual keys
4. Bring your finger close to your palm to "press" a key

### Controls
- **ESC**: Exit the application
- **Space**: Toggle keyboard visibility
- **Index Finger**: Point to keys
- **Finger close to palm**: Press key

### Tips for Best Performance
- Ensure good lighting
- Keep your hand within camera view
- Maintain 30-60cm distance from camera
- Use a solid background
- Point your index finger clearly

## Support

If you encounter issues:
1. Check the troubleshooting section above
2. Run `python test_setup.py` to diagnose problems
3. Check that all dependencies are installed correctly
4. Ensure your webcam is working with other applications

## System Requirements

- **OS**: Windows 10+, macOS 10.14+, or Linux
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Camera**: 720p or higher webcam
- **Storage**: 100MB free space 