import cv2
import mediapipe as mp
import random
import os
import time
from schedulers import opensong
from timer import Timer
from playsound import playsound
from PIL import Image
import numpy as np
rectangle_frames = 0
rectangle_coords = (200,200)

def image_loader(coord, image):
    #image = Image.open(os.getcwd() + "/msword.jpeg", cv2.IMREAD_UNCHANGED)
    img2 = cv2.imread(os.getcwd() + "/msword.jpeg", cv2.IMREAD_UNCHANGED)
    size = 500
    cv2.resize(img2, (size,size))
    #img2gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    ret, mask = cv2.threshold(img2, 120, 255, cv2.THRESH_BINARY)
    #image.paste(img2, coord, mask = img2)
    roi = image[-size-10:-100, -size-10:-10]
  
    # Set an index of where the mask is
    roi[np.where(mask)] = 0
    roi += img2
    return image

def detect_hit(landmark,rectangle_coords1,rectangle_coords2):
  normalized_x1 = rectangle_coords1[0]/1280.0
  normalized_y1 = rectangle_coords1[1]/720.0
  normalized_x2 = rectangle_coords2[0]/1280.0
  normalized_y2 = rectangle_coords2[1]/720.0
  return normalized_x1 < landmark[17].x < normalized_x2 and normalized_y1 < landmark[17].y < normalized_y2

screen_width = 640
screen_height = 360




# clicks = opensong(os.getcwd() + "/songs/sasageyo.txt")
# for click in clicks:
#   print(click)

def handle(results, image):
  #print('here')

  BLUE = (255, 0, 0)
  radius = 25

  try: 
    leftx = (results.pose_landmarks.landmark[19].x + results.pose_landmarks.landmark[15].x) / 2
    lefty = (results.pose_landmarks.landmark[19].y + results.pose_landmarks.landmark[15].y) / 2

    rightx = (results.pose_landmarks.landmark[22].x + results.pose_landmarks.landmark[18].x) / 2
    righty = (results.pose_landmarks.landmark[20].y + results.pose_landmarks.landmark[16].y) / 2

    centerR = (int(rightx*(screen_width)),int(righty*(screen_height)))
    centerL = (int(leftx*(screen_width)),int(lefty*(screen_height)))

    if (rightx < .5 and righty < .5):
      print("top right - RH")
    if (rightx < .5 and righty > .5):
      print("bottom right - RH")
    if (rightx > .5 and righty < .5):
      print("top left - RH")
    if (rightx > .5 and righty > .5):
      print("bottom left - RH")


    image = cv2.circle(image, centerR, radius, BLUE, -1)
    image = cv2.circle(image, centerL, radius, BLUE, -1)

    font = cv2.FONT_HERSHEY_SIMPLEX
    image = cv2.putText(image,'R',(centerR[0] - radius, centerR[1] + radius), font, 2,(255,255,255),2,cv2.LINE_AA)

    # image = image_loader(centerR, image)
    # image = image_loader(centerL, image)
    return image
  except:
    # center = (0,0)
    # image = cv2.circle(image, center, radius, BLUE, 2)
    
    # image = image_loader(center, image)
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

currentHitObject = 0
timer = Timer()
#playsound(os.getcwd() + "\songs\sasageyo.mp3", block=False)
timer.start()

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

    #image = imageStore[1]
    # Draw the pose annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    mp_drawing.draw_landmarks(
        image,
        results.pose_landmarks,
        mp_pose.POSE_CONNECTIONS,
        landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style())
    # Flip the image horizontally for a selfie-view display.
    # if rectangle_frames == 0:
    #   if random.randint(0,60) > 55:
    #     rectangle_frames = 50
    #     rectangle_coords = (int(random.random()*(1280-100)),int(random.random()*(720-100)))
    #     rectangle_coords2 = (rectangle_coords[0]+100,rectangle_coords[1]+100)
    # else:
    #   print("rectangle:",rectangle_coords,rectangle_coords2)
    #   print(1-results.pose_landmarks.landmark[17].x,results.pose_landmarks.landmark[17].y)
    #   image = cv2.rectangle(image, rectangle_coords, rectangle_coords2, (255,0,0), 7)
    #   hit = detect_hit(results.pose_landmarks.landmark,rectangle_coords,rectangle_coords2)
    #   if hit:
    #     rectangle_frames = 1
    #     print("hit")
    #   rectangle_frames-=1 
    # if timer.getTime() * 1000 < clicks[currentHitObject].time + 50 and                           timer.getTime() * 1000 > clicks[currentHitObject].time - 50:
    #   curr = clicks[currentHitObject]
    #   image = cv2.rectangle(image, (curr.x, curr.y), (curr.x+100,curr.y+100), (0,255,0), 7)
    #   currentHitObject+=1

        
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()

