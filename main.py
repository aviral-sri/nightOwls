import cv2
import time
import threading
import pygame

# Initialize pygame mixer
pygame.mixer.init()
beep_sound = pygame.mixer.Sound('beep.wav')

# Load Haar Cascades for face and eye detection
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)
eye_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_eye.xml'
)

# Initialize video capture
cap = cv2.VideoCapture(0)

# Timing variables
last_eye_detection = time.time()
ALARM_DURATION = 5  # seconds

# Flag to debounce the beep call
beep_playing = False

def reset_beep():
    global beep_playing
    beep_playing = False

def trigger_beep():
    global beep_playing
    if not beep_playing:
        beep_playing = True
        beep_sound.play()
        # Schedule flag reset after the beep finishes playing
        threading.Timer(beep_sound.get_length(), reset_beep).start()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 3)
    eyes_detected = False

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # Use only the upper half of the face for eye detection
        roi_gray = gray[y:y + h//2, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=5)
        if len(eyes) > 0:
            eyes_detected = True
            last_eye_detection = time.time()
        for (ex, ey, ew, eh) in eyes:
            # Draw rectangles on the original frame for clarity
            cv2.rectangle(frame, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (0, 255, 0), 2)

    # If eyes haven't been detected for ALARM_DURATION seconds, trigger a beep
    if time.time() - last_eye_detection > ALARM_DURATION:
        cv2.putText(frame, "WAKE UP!", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        trigger_beep()

    cv2.imshow('Eye Monitor', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
