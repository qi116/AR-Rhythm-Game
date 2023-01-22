import cv2
import mediapipe as mp
import random
import os
import time
from schedulers import opensong
from timer import Timer
from schedulers import *
screen_width = 640
screen_height = 360

def detect_hit(landmark,rectangle_coords1,rectangle_coords2,size=(screen_width,screen_height)):
  normalized_x1 = rectangle_coords1[0]/size[0]
  normalized_y1 = rectangle_coords1[1]/size[1]
  normalized_x2 = rectangle_coords2[0]/size[0]
  normalized_y2 = rectangle_coords2[1]/size[1]
  return normalized_x1 < landmark[17].x < normalized_x2 and normalized_y1 < landmark[17].y < normalized_y2



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
timer.start()
hittable_stack = []
scheduler = OsuScheduler("./sasageyo.txt",size=(screen_width,screen_height))
#play music right here
with mp_pose.Pose(
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as pose:
  while cap.isOpened():
    success, image = cap.read()
    image = cv2.resize(image, (screen_width,screen_height), interpolation =cv2.INTER_AREA)
    t = timer.getTime()
    while scheduler.next_time() < t:
      hittable_stack.append(next(scheduler))
    for i in range(len(hittable_stack)):
      if hittable_stack[i].time_tup[1] >= t:
        break
    hittable_stack = hittable_stack[i:]
    for item in hittable_stack:
      image = item.apply(image,t)
        

    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = pose.process(image)

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
    try:
      rectangle_coords =   hittable_stack[0].location_tup
      rectangle_coords2 = (rectangle_coords[0]+100,rectangle_coords[1]+100)
      # print("rectangle:",rectangle_coords,rectangle_coords2,"time:",t)
      # print(1-results.pose_landmarks.landmark[17].x,results.pose_landmarks.landmark[17].y)
      # image = cv2.rectangle(image, rectangle_coords, rectangle_coords2, (255,0,0), 7)
      hit = detect_hit(results.pose_landmarks.landmark,rectangle_coords,rectangle_coords2)
      if hit:
        print("hit") 
    # if timer.getTime() * 1000 < clicks[currentHitObject].time + 50 and                           timer.getTime() * 1000 > clicks[currentHitObject].time - 50:
    #   curr = clicks[currentHitObject]
    #   image = cv2.rectangle(image, (curr.x, curr.y), (curr.x+100,curr.y+100), (0,255,0), 7)
    #   currentHitObject+=1
    except:
      print("no landmark")
        
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()

