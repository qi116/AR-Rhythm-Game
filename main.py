import cv2
import mediapipe as mp
import random
rectangle_frames = 0
rectangle_coords = (200,200)
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
# print ("Frame default resolution: (" + str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) + "; " + str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) + ")")
# cap.set(3, 800)
# cap.set(4, 600)
# print ("Frame resolution set to: (" + str(cap.get(cv2.CAP_PROP_FRAME_WIDTH)) + "; " + str(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)) + ")")
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)
    try:
      print(results.pose_landmarks.landmark[17].x)
    except Exception:
      print("None")

    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # Flip the image horizontally for a selfie-view display.
    image = cv2.resize(image, (1280,720), interpolation =cv2.INTER_AREA)
    if rectangle_frames == 0:
      if random.randint(0,60) > 55:
        rectangle_frames = 20
        rectangle_coords = (int(random.random()*(1280-100)),int(random.random()*(720-100)))
    else:
      rectangle_frames-=1
      image = cv2.rectangle(image, rectangle_coords, (rectangle_coords[0]+100,rectangle_coords[1]+100), (255,0,0), 7)
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()

def handle(result):
  print('here')