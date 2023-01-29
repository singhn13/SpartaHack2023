import cv2
import numpy as np
import pyautogui
import asyncio as a


cursor_speed = 20


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')


# Start the webcam
cap = cv2.VideoCapture(0)

x = 0
face_x1, face_y1 = 0, 0
while x < 50:
    ret1, frame1 = cap.read()

    gray = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)

        # Detect faces in the frame
    faces1 = face_cascade.detectMultiScale(gray, 1.3, 5)
    face_x1 = 0
    face_y1 = 0
    # Iterate over each face
    for (x1, y1, w1, h1) in faces1:
        face_x1 = int(x1 + w1/2)
        face_y1 = int(y1 + h1/2)
    x += 1

count = 0
while True:
    # Read a frame from the webcam
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detect faces in the frame
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    # Iterate over each face
    for (x, y, w, h) in faces:
        # Draw a rectangle around the face
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
        # Get the face center coordinates
        face_x = int(x + w/2)
        face_y = int(y + h/2)
        # Calculate the face angle
        face_angle = np.arctan2(face_y - frame.shape[0]/2, face_x - frame.shape[1]/2)
        # Calculate the cursor movement based on the face angle
        cursor_x = cursor_speed * np.cos(face_angle) * -1
        cursor_y = 18 * np.sin(face_angle) 
        # Move the cursor

        if (face_x1-4 > face_x or face_x > face_x1+4) and (face_y1-4 > face_y or face_y > face_y1+4):
            pyautogui.moveRel(cursor_x, cursor_y)
        # Get the region of interest for the eyes
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 5)

    # Draw rectangles around the eyes
    temp_flag = np.any(eyes)
    if temp_flag == False:
        if count >= 20:
            pyautogui.click()
        count += 1
    for (x, y, w, h) in eyes:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)



    # Show the frame
    cv2.imshow('frame', frame)

    # Exit the loop if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()