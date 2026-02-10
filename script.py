import cv2
import mediapipe as mp
import numpy as np
import time
from playsound import playsound
import threading

# =========================
# Configuration parameters
# =========================
EYE_CLOSED_THRESHOLD = 0.22      # EAR threshold for closed eyes
CLOSED_TIME_REQUIRED = 2.0       # seconds (ignores blinking)
ALARM_SOUND_PATH = "alarm.wav"   # provide your own .wav file

# =========================
# Initialize MediaPipe
# =========================
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# =========================
# Eye landmark indices
# =========================
LEFT_EYE = [33, 160, 158, 133, 153, 144]
RIGHT_EYE = [362, 385, 387, 263, 373, 380]

# =========================
# Utility functions
# =========================
def euclidean_distance(p1, p2):
    return np.linalg.norm(np.array(p1) - np.array(p2))


def eye_aspect_ratio(eye_landmarks):
    vertical_1 = euclidean_distance(eye_landmarks[1], eye_landmarks[5])
    vertical_2 = euclidean_distance(eye_landmarks[2], eye_landmarks[4])
    horizontal = euclidean_distance(eye_landmarks[0], eye_landmarks[3])
    return (vertical_1 + vertical_2) / (2.0 * horizontal)


def play_alarm():
    playsound(ALARM_SOUND_PATH)


# =========================
# Main loop
# =========================
cap = cv2.VideoCapture(0)

eyes_closed_start = None
alarm_triggered = False

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(frame_rgb)

    h, w, _ = frame.shape

    if results.multi_face_landmarks:
        face_landmarks = results.multi_face_landmarks[0]

        landmarks = []
        for lm in face_landmarks.landmark:
            landmarks.append((int(lm.x * w), int(lm.y * h)))

        left_eye_points = [landmarks[i] for i in LEFT_EYE]
        right_eye_points = [landmarks[i] for i in RIGHT_EYE]

        left_ear = eye_aspect_ratio(left_eye_points)
        right_ear = eye_aspect_ratio(right_eye_points)
        ear = (left_ear + right_ear) / 2.0

        # =========================
        # Eye closure logic
        # =========================
        if ear < EYE_CLOSED_THRESHOLD:
            if eyes_closed_start is None:
                eyes_closed_start = time.time()

            closed_duration = time.time() - eyes_closed_start

            if closed_duration >= CLOSED_TIME_REQUIRED:
                if not alarm_triggered:
                    alarm_triggered = True
                    threading.Thread(target=play_alarm, daemon=True).start()

                cv2.putText(
                    frame,
                    "CAUTION: EYES CLOSED",
                    (50, 120),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1.6,
                    (0, 0, 255),
                    4
                )
        else:
            # Reset when eyes are open (blink ignored)
            eyes_closed_start = None
            alarm_triggered = False

    cv2.imshow("Eye Closure Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
