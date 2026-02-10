# Eye Closure Alarm System

## Overview

This project implements a real-time **eye closure detection system** using a webcam.  
The system detects when a person's eyes remain closed for **more than two seconds** and then triggers:

- An **audio alarm**
- A **visual warning message** displayed in red on the video stream

Short eye closures such as **normal blinking are ignored**.  
The system is suitable for basic **drowsiness monitoring**, **attention control**, or **safety demonstrations**.

---

## Features

- Real-time webcam processing
- Eye state detection using facial landmarks
- Blink filtering (ignores short eye closures)
- Alarm activation only after prolonged eye closure
- Visual warning message: `CAUTION: EYES CLOSED`
- Lightweight and runs on CPU

---

## Technology Stack

- Python 3
- OpenCV
- MediaPipe Face Mesh
- NumPy
- playsound

---

## How It Works

1. The webcam captures video frames in real time.
2. MediaPipe Face Mesh detects facial landmarks.
3. Eye Aspect Ratio (EAR) is calculated for both eyes.
4. If the EAR value falls below a defined threshold, the eyes are considered closed.
5. If the eyes remain closed for **more than 2 seconds**, the system:
   - Plays an alarm sound
   - Displays a red warning message on the screen
6. When the eyes reopen, the timer and alarm state reset.

---

## Installation

Install the required Python packages:

```bash
pip install opencv-python mediapipe numpy playsound==1.2.2
