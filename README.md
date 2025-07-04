# 🖱️ Virtual Mouse using Hand Gestures (macOS Compatible)

Control your mouse with hand gestures using OpenCV, MediaPipe, and PyAutoGUI.  
No hardware required beyond your laptop camera!

---

## 📸 Features

- ✅ Move mouse pointer using **index + middle finger up**
- ✅ Left click using **index finger down**
- ✅ Right click using **middle finger down**
- ✅ Scroll up using **both fingers down + thumb open**
- ✅ Scroll down using **both fingers up + thumb open**
- ✅ Ignores **left hand** completely
- ✅ Works on **macOS** using webcam

---

## 🧠 How It Works

This app uses:
- **MediaPipe** to detect hand landmarks in real time
- **PyAutoGUI** to move and control mouse
- **OpenCV** to display feedback and camera stream

Each gesture maps to a traditional mouse event:
| Gesture                                  | Action       |
|------------------------------------------|--------------|
| Index ↑ + Middle ↑ + Thumb closed        | Mouse Move   |
| Index ↓ + Middle ↑ + Thumb closed        | Left Click   |
| Index ↑ + Middle ↓ + Thumb closed        | Right Click  |
| Both ↓ + Thumb Open                      | Scroll Up    |
| Both ↑ + Thumb Open                      | Scroll Down  |

---

## ⚙️ Requirements

```bash
pip install opencv-python mediapipe pyautogui numpy
