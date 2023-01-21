import cv2
import mediapipe as mp
import random
rectangle_frames = 0
rectangle_coords = (200,200)

def detect_hit(landmark,rectangle_coords1,rectangle_coords2):
  normalized_x1 = rectangle_coords1[0]/1280.0
  normalized_y1 = rectangle_coords1[1]/720.0
  normalized_x2 = rectangle_coords2[0]/1280.0
  normalized_y2 = rectangle_coords2[1]/720.0
  return normalized_x1 < landmark[17].x < normalized_x2 and normalized_y1 < landmark[17].y < normalized_y2

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
    image = cv2.resize(image, (1280,720), interpolation =cv2.INTER_AREA)
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
    # handle(results)
    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # Flip the image horizontally for a selfie-view display.
    if rectangle_frames == 0:
      if random.randint(0,60) > 55:
        rectangle_frames = 50
        rectangle_coords = (int(random.random()*(1280-100)),int(random.random()*(720-100)))
        rectangle_coords2 = (rectangle_coords[0]+100,rectangle_coords[1]+100)
    else:
      print("rectangle:",rectangle_coords,rectangle_coords2)
      print(1-results.pose_landmarks.landmark[17].x,results.pose_landmarks.landmark[17].y)
      image = cv2.rectangle(image, rectangle_coords, rectangle_coords2, (255,0,0), 7)
      hit = detect_hit(results.pose_landmarks.landmark,rectangle_coords,rectangle_coords2)
      if hit:
        rectangle_frames = 1
        print("hit")
      rectangle_frames-=1 
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()

