import cv2
import mediapipe as mp
import random
import os

rectangle_frames = 0
rectangle_coords = (200,200)

screen_width = 640
screen_height = 360

class Hit:
  def __init__(self, x, y, time): #time is in miliseconds
    self.x = x
    self.y = y
    self.time = time
  def __str__(self):
     return "x: " + str(self.x) + " y: " + str(self.y) + " time (ms): " + str(self.time)
def opensong(path):
  file = open(path, 'r')
  lines = file.readlines()
  clicks = []
  for line in lines:
    lineSplit = line.split(",")
    h = Hit(lineSplit[0], lineSplit[1], lineSplit[2])
    clicks.append(h)
  return clicks

clicks = opensong(os.getcwd() + "\songs\photograph.txt")
for click in clicks:
  print(click)

def handle(results, image):
  #print('here')
  BLUE = (255, 0, 0)
  
  axes = 50, 50
  angle = 0
  try: 
    leftx = (results.pose_landmarks.landmark[19].x + results.pose_landmarks.landmark[15].x) / 2
    lefty = (results.pose_landmarks.landmark[19].y + results.pose_landmarks.landmark[15].y) / 2

    rightx = (results.pose_landmarks.landmark[22].x + results.pose_landmarks.landmark[18].x) / 2
    righty = (results.pose_landmarks.landmark[20].y + results.pose_landmarks.landmark[16].y) / 2

    center = (int(rightx*(screen_width)),int(righty*(screen_height)))

    if (rightx < .5 and righty < .5):
      print("top right - RH")
    if (rightx < .5 and righty > .5):
      print("bottom right - RH")
    if (rightx > .5 and righty < .5):
      print("top left - RH")
    if (rightx > .5 and righty > .5):
      print("bottom left - RH")


    image = cv2.circle(image, center, 50, BLUE, 2)
    return image
  except:
    center = (0,0)
    image = cv2.circle(image, center, 50, BLUE, 2)
    return image


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
    image = cv2.resize(image, (screen_width,screen_height), interpolation =cv2.INTER_AREA)

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
    image = handle(results, image)
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
        rectangle_frames = 20
        rectangle_coords = (int(random.random()*(screen_width-100)),int(random.random()*(screen_height-100)))
    else:
      rectangle_frames-=1
      image = cv2.rectangle(image, rectangle_coords, (rectangle_coords[0]+100,rectangle_coords[1]+100), (255,0,0), 7)
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()

