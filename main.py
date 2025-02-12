import cv2
import time
import threading
import pygame

print("Welcome to night owl!")

while True:
    
    inti = input("Type (START) for normal mode, (START H) for Danger mode : ")

    if inti == "START" or inti == "START H":
        if inti == "START H":
            print("Danger mode activated!")
            Hazard_ON = True
        else:
            print("Normal mode activated!")
            Hazard_ON = False

        # Initialize pygame mixer
        pygame.mixer.init()
        # prompt user to select a alarm sound (currently 2 option, beep and sound)
        while True:
            print("Choose an alarm sound:")
            print("1. Beep")
            print("2. Silent")
            choice = input("Enter your choice (1/2): ")
            if choice == "1":
                print("Beep mode selected!")
                beep_sound = pygame.mixer.Sound('beep.wav')
                break
            elif choice == "2":
                if inti == "START H":
                    print("Sorry, you can not select for silent in danger mode")
                elif inti != "START H":
                    print("Silent mode selected!")
                    beep_sound = pygame.mixer.Sound('silent.wav')
                    break

            else:
                print("Invalid choice. Please try again.")

        

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

        def trigger_beep_loud():
            global beep_playing
            if not beep_playing:
                beep_playing = True
                beep_sound.set_volume(min(1.0, beep_sound.get_volume() * 2))
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
            
            if Hazard_ON:
                ALARM_DURATION = 2  # seconds
                Hazard_DURATION = 5 # seconds
                if time.time() - last_eye_detection > ALARM_DURATION:
                    cv2.putText(frame, "WAKE UP!", (10, 30),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 100, 255), 2)
                    trigger_beep() 
                if time.time() - last_eye_detection > Hazard_DURATION:
                    cv2.putText(frame, "DANGER!", (10, 60),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                    trigger_beep_loud()
            else:
                 if time.time() - last_eye_detection > ALARM_DURATION:
                    cv2.putText(frame, "WAKE UP!", (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 100, 255), 2)
                    trigger_beep()

            cv2.imshow('Eye Monitor', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
    else:
        print("Invalid input. Please try again.")
