# mouse-control-using-hand-gestures
# 🖐️ Virtual Mouse using Hand Tracking (Webcam-Based)

This project implements a **virtual mouse system** using a standard webcam and hand gesture recognition. Instead of using a physical mouse, the system tracks your hand in real-time and translates specific finger movements into cursor actions like moving, clicking, and more.

---

## 🚀 Overview

The core idea is simple:

* Use your **webcam** to capture live video
* Detect and track your **hand landmarks**
* Map hand movements to **cursor movement**
* Use **thumb gestures** to simulate mouse clicks

This creates a fully touchless interaction system using just your hand.

---

## 🧠 How It Works

### 1. Video Capture

The webcam continuously captures frames in real-time. Each frame is processed individually.

### 2. Hand Detection & Landmark Tracking

Using a hand tracking model, the system identifies key points (landmarks) on your hand such as fingertips and joints.

### 3. Cursor Movement

* The position of a specific finger (usually the **index finger**) is mapped to screen coordinates.
* As you move your finger, the cursor moves accordingly.
* Smoothing techniques may be applied to reduce jitter.

### 4. Click Detection (Thumb Gesture)

* The system monitors the **distance between the thumb and index finger** (or another reference point).
* When the thumb comes close enough, it is interpreted as a **mouse click**.

This replaces traditional mouse button input with a natural gesture.

---

## ✨ Features

* 🎯 Real-time hand tracking
* 🖱️ Cursor movement using finger position
* 👍 Click detection using thumb gesture
* ⚡ Smooth and responsive interaction
* 💻 Works with just a webcam (no extra hardware)

---

## 🛠️ Tech Stack

* Python
* OpenCV (for video processing)
* Hand tracking framework (e.g., MediaPipe)
* OS interaction libraries (for controlling mouse)

---

## 📂 Project Structure

```
├── main.py              # Entry point
├── hand_tracking.py     # Hand detection logic
├── utils.py             # Helper functions
├── requirements.txt     # Dependencies
└── README.md            # Project documentation
```

---

## ▶️ How to Run

1. Clone the repository:

   ```
   git clone <your-repo-link>
   cd <repo-name>
   ```

2. Install dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Run the project:

   ```
   python main.py
   ```

---

## ⚙️ Controls

| Gesture             | Action      |
| ------------------- | ----------- |
| Move index finger   | Move cursor |
| Thumb touch gesture | Left click  |

---

## ⚠️ Limitations

* Requires good lighting conditions
* Performance depends on webcam quality
* May need calibration for different screen sizes

---

## 🔮 Future Improvements

* Right-click gesture
* Scroll functionality
* Drag-and-drop support
* Multi-hand gestures
* Improved stability and accuracy

---

## 🙌 Acknowledgements

Inspired by modern gesture-based interaction systems and computer vision applications.

---

## 📌 Note

This project is a demonstration of how computer vision can replace traditional input devices. It is not meant to fully replace a physical mouse but showcases the possibilities of touchless interfaces.

---

Feel free to fork, improve, and experiment with it!
