import cv2
import mediapipe as mp
import random
import os
import time
from schedulers import *
from timer import Timer
from playsound import playsound
from PIL import Image
import numpy as np
from scoreboard import Scoreboard

rectangle_frames = 0
rectangle_coords = (200,200)


screen_width = 640
screen_height = 360

scoreboard = Scoreboard(0, 1)

#counter = 1

def detect_hit(landmark,rectangle_coords1,rectangle_coords2,size=(screen_width,screen_height)):
  normalized_x1 = rectangle_coords1[0]/size[0]
  normalized_y1 = rectangle_coords1[1]/size[1]
  normalized_x2 = rectangle_coords2[0]/size[0]
  normalized_y2 = rectangle_coords2[1]/size[1]
  return normalized_x1 < landmark[7].x < normalized_x2 and normalized_y1 < landmark[7].y < normalized_y2



# clicks = opensong(os.getcwd() + "/songs/sasageyo.txt")
# for click in clicks:
#   print(click)

# def handle(results, image):
#   #print('here')

#   BLUE = (255, 0, 0)
#   radius = 25
#   lands = results.multi_hand_landmarks
#   #print(lands)
#   if lands:
    
#     for land in lands:
      
#       try: 
#         #print(land.landmark[0].x)
#         width = (land.landmark[5].x + land.landmark[20].x)/2
#         height = (land.landmark[0].y + land.landmark[12].y)/2
#         center = (int(width*(screen_width)),int(height*(screen_height)))
#         image = cv2.circle(image, center, radius, BLUE, -1)
        
#         # font = cv2.FONT_HERSHEY_SIMPLEX
#         # image = cv2.putText(image,'R',(centerR[0] - radius, centerR[1] + radius), font, 2,(255,255,255),2,cv2.LINE_AA)

#       except:
#         print("fail")
#   return image

  
#input stuff:
name = 'sasageyo'
# while 1:
#   num = input("Pick a song number: ")
#   if num == '1':
#     name = 'sasageyo'
#     break
#   if num == '2':
#     name = 'photograph'
#     break
  

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)

currentHitObject = 0
timer = Timer()
timer.start()
playsound('./songs/' + name + '.mp3', block=False)

pressed = False

hittable_stack = []
scheduler = OsuScheduler("./songs/" + name+ ".txt",size=(screen_width,screen_height))
#play music right here
with mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as hands:
  #print(hands)
  while cap.isOpened():
    success, image = cap.read()
    image = cv2.resize(image, (screen_width,screen_height), interpolation =cv2.INTER_AREA)
    t = timer.getTime()
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    while scheduler.next_time() < t:
      hold = next(scheduler)
      if hold == None:
        break
      hittable_stack.append(next(scheduler))
    for i in range(len(hittable_stack)):
      if hittable_stack[i] and hittable_stack[i].time_tup[1] >= t:
        break
    if i != 0:
      print('miss')
      scoreboard.resetMultiplier()
    hittable_stack = hittable_stack[i:]
    for item in hittable_stack:
      if item == None:
        break
      image = item.apply(image,t)
        

    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    

    
    
    #image = handle(results, image)
    image = cv2.flip(image, 1)
    image = cv2.putText(image, str(scoreboard.getScore()), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)
    image = cv2.putText(image, str(scoreboard.getMultiplier()) + "x", (600, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,(255,255,255),2,cv2.LINE_AA)

    image = cv2.flip(image, 1)
    #image = imageStore[1]
    # Draw the pose annotation on the image.
    
    # Flip the image horizontally for a selfie-view display.
    if len(hittable_stack):
      try:
        if not hittable_stack:
          break
        rectangle_coords =   hittable_stack[0].location_tup
        rectangle_coords2 = (rectangle_coords[0]-100,rectangle_coords[1]-100)
        # print("rectangle:",rectangle_coords,rectangle_coords2,"time:",t)
        # print(1-results.pose_landmarks.landmark[17].x,results.pose_landmarks.landmark[17].y)
        # image = cv2.rectangle(image, rectangle_coords, rectangle_coords2, (255,0,0), 7)
        if results.multi_hand_landmarks:
          for lands in results.multi_hand_landmarks:
            hit = detect_hit(lands.landmark,rectangle_coords2,rectangle_coords)
            if pressed and hit and hittable_stack[0].hittable:
              print("hit") 
              hittable_stack.pop(0)
              scoreboard.addScore(100)
              scoreboard.setMultiplier(scoreboard.getMultiplier() + 1)
              break
      # if timer.getTime() * 1000 < clicks[currentHitObject].time + 50 and                           timer.getTime() * 1000 > clicks[currentHitObject].time - 50:
      #   curr = clicks[currentHitObject]
      #   image = cv2.rectangle(image, (curr.x, curr.y), (curr.x+100,curr.y+100), (0,255,0), 7)
      #   currentHitObject+=1
      except Exception as e:
        print(e)
        break
    if results.multi_hand_landmarks:
      #print("here2")
      for hand_landmarks in results.multi_hand_landmarks:
        #print('here')
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())
    pressed = False    
    cv2.imshow('MediaPipe Pose', cv2.flip(image, 1))
    if cv2.waitKey(32) == 32:
      print('Pressed space')
      pressed = True
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()

