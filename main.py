import cv2
import time
import threading
import pygame
import pywhatkit
import numpy as np
from twilio.rest import Client
import time

class DrowsinessDetector:
    def __init__(self):
        print("Initializing DrowsinessDetector...")
        self.hazard_on = False
        self.sound_on = True
        self.beep_playing = False
        self.last_eye_detection = time.time()
        self.ALARM_DURATION = 2
        self.HAZARD_DURATION = 4
        self.DANGER_DURATION = 10
        self.detection_active = False
        self.latest_frame = None
        self.frame_lock = threading.Lock()

        # Load Haar Cascades
        self.face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

        # Initialize pygame for sound
        pygame.mixer.init()
        self.beep_sound = pygame.mixer.Sound('static/beep.wav')

        # Camera initialized on start_detection
        self.cap = None

    def reset_beep(self):
        self.beep_playing = False

    def notify(self):
        account_sid = "Auth ID" 
        auth token = "Auth Token" 
        twilio_number "Given Phone Number" 
        recipient_number = "Recipient Number"

        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_=twilio_number,
            body="Driver is falling asleep!!",
            to=recipient_number
        )

        print("Message sent! SID:", message.sid)


    def trigger_beep(self):
        if self.sound_on and not self.beep_playing:
            self.beep_playing = True
            self.beep_sound.play()
            threading.Timer(self.beep_sound.get_length(), self.reset_beep).start()

    def trigger_beep_loud(self):
        if self.sound_on and not self.beep_playing:
            self.beep_playing = True
            self.beep_sound.set_volume(min(1.0, self.beep_sound.get_volume() * 2))
            self.beep_sound.play()
            threading.Timer(self.beep_sound.get_length(), self.reset_beep).start()


    def start_detection(self, hazard_on=False, sound_on=True):
        self.hazard_on = hazard_on
        self.sound_on = sound_on
        self.detection_active = True
    

        # Initialize camera
        if not self.cap or not self.cap.isOpened():
            self.cap = cv2.VideoCapture(0)
            start = time.time() 
            notification_sent = False
            while self.detection_active:
                ret, frame = self.cap.read()
                if not ret or frame is None:
                    print("Warning: Unable to capture frame from camera.")
                    continue 

                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                eyes_detected = False

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
                    roi_gray = gray[y:y+h//2, x:x+w]
                    eyes = self.eye_cascade.detectMultiScale(roi_gray, 1.3, 5)

                    if len(eyes) >= 2:
                        eyes_detected = True
                        self.last_eye_detection = time.time()

                    for (ex, ey, ew, eh) in eyes:
                        cv2.rectangle(frame, (x+ex, y+ey), (x+ex+ew, y+ey+eh), (0, 255, 0), 2)

                # Alert logic

                elapsed = time.time() - self.last_eye_detection
                if self.hazard_on:
                    
                    if elapsed > self.DANGER_DURATION and (time.time() - start)> 8 :
                        cv2.putText(frame, "Notification Sent!, now you have to restart the system.", (10, 90),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        self.trigger_beep_loud()
                        if not notification_sent:
                            self.notify()
                            notification_sent = True
                    if elapsed > self.HAZARD_DURATION:
                        cv2.putText(frame, "DANGER!", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                        self.trigger_beep_loud()
                    if elapsed > self.ALARM_DURATION:
                        cv2.putText(frame, "WAKE UP!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 100, 255), 2)
                        self.trigger_beep()
                else:
                    self.ALARM_DURATION = 5
                    if elapsed > self.ALARM_DURATION:
                        cv2.putText(frame, "WAKE UP!", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 100, 255), 2)
                        self.trigger_beep()

                # Update latest frame
                with self.frame_lock:
                    self.latest_frame = frame.copy()


        # Cleanup
        if self.cap and self.cap.isOpened():
            self.cap.release()
        cv2.destroyAllWindows()
        self.detection_active = False

    def stop_detection(self):
        self.detection_active = False

drowsiness_detector = DrowsinessDetector()
