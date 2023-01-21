import cv2
import mediapipe as mp


def handle(results):
  #print('here')
  try: 
    leftx = (results.pose_landmarks.landmark[19].x + results.pose_landmarks.landmark[15].x) / 2
    lefty = (results.pose_landmarks.landmark[19].y + results.pose_landmarks.landmark[15].y) / 2

    rightx = (results.pose_landmarks.landmark[20].x + results.pose_landmarks.landmark[16].x) / 2
    righty = (results.pose_landmarks.landmark[20].y + results.pose_landmarks.landmark[16].y) / 2
  except:
    return

  if (rightx < .5 and righty < .5):
    print("top right - RH")
  if (rightx < .5 and righty > .5):
    print("bottom right - RH")
  if (rightx > .5 and righty < .5):
    print("top left - RH")
  if (rightx > .5 and righty > .5):
    print("bottom left - RH")

  if (leftx < .5 and lefty < .5):
    print("top right - LH")
  if (leftx < .5 and lefty > .5):
    print("bottom right - LH")
  if (leftx > .5 and lefty < .5):
    print("top left - LH")
  if (leftx > .5 and lefty > .5):
    print("bottom left - LH")
  

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)
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

    #print(results.pose_landmarks.landmark[17].y)
    handle(results)
    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()

