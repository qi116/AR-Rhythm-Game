import cv2
import mediapipe as mp
import random
#from main import *


def opensong(path):
        file = open(path, 'r')
        lines = file.readlines()
        clicks = []
        for line in lines:
            lineSplit = line.split(",")
            #h = Hit(int(lineSplit[0]), int(lineSplit[1]), int(lineSplit[2]), int(lineSplit[3]))
            h = None # make h to be Hittable stuff
            clicks.append(h)
        return clicks

class Scheduler:
    def __init__(self,times,locations):
        self.i = 0
        self.times = times
        self.locations = locations

    def __iter__(self):
        return self

    def __next__(self):
        print("next")
        raise NotImplementedError
    

class OsuScheduler(Scheduler):
    def __init__(self,path,duration=1.0,size=(1280,720)):
        data = []
        self.duration = duration
        with open(path,"r") as f:
            data = f.read().split("\n")
            data = [x.split(",") for x in data]
            for row in data:
                for i in range(len(row)):
                    if i < 4:
                        row[i] = int(row[i])
                row[0]=int(row[0]/640*size[0])
                row[1]= int(row[1]/480*size[1])

        self.data = data
        super().__init__([],[])

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < len(self.data):
            center = self.data[self.i][2]/1000.0
            time_tup = (center - self.duration/2,center + self.duration/2)
            location_tup = (self.data[self.i][0]+100,self.data[self.i][1]+100) #to make them stay on screen
            type = self.data[self.i][3] 
            out = Hittable(time_tup,location_tup,type)
            self.i += 1
            return out
        else:
            return None
            #raise StopIteration

    def next_time(self):
        if self.i >= len(self.data):
            return 0
        return self.data[self.i][2]/1000.0 - self.duration/2 - 1.5

class RandomScheduler(Scheduler):
    def __init__(self,duration,length,size=(1280,720)):
        times = []
        locations = []
        time = 0
        for i in range(length):
            time+= random.random()*3+1
            times.append((time,time+duration))
            locations.append((int(random.random()*(size[0]-100)),int(random.random()*(size[1]-100))))
            time+= duration
        super().__init__(times,locations)
        print(times,locations)   

    def __iter__(self):
        return self

    def __next__(self):
        if self.i < len(self.times):
            out = Hittable(self.times[self.i],self.locations[self.i])
            self.i += 1
            return out
        else:
            raise StopIteration
            
class Hittable:
    
    def __init__(self,time_tup,location_tup,type) -> None:
            self.time_tup = time_tup
            self.location_tup = location_tup
            self.type = type
            self.phases = 10
            self.load_time = 1.5
            self.hittable = False
            global counter
            if (self.type == 5 or self.type == 6):
                counter = 1
            else:
                counter += 1
            self.currCounter = counter
    def isShown(self,time):
        return self.time_tup[0]-1.5 <= time <= self.time_tup[1] #includes loading time

    def apply(self,image,time):
        if self.time_tup[0]-1.5 < time < self.time_tup[0]:
            
            phase = (self.time_tup[0]-time)/1.5

            color = (255*phase,255*(1-phase),0)
            image = cv2.rectangle(image, self.location_tup, [x -100 for x in self.location_tup], color, 7)
            
            #filling rectangle
            center = [x - 50 for x in self.location_tup]
            phase = (1-phase) * 50
            image = cv2.rectangle(image, [x + int(phase) for x in center], [x - int(phase) for x in center], color, -1)
            
            overlay = image.copy()
            cv2.rectangle(overlay, [x + int(phase) for x in center], [x - int(phase) for x in center], color, -1)  
            alpha = 0.4
            image = cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0)


            image = cv2.flip(image, 1)
            image = cv2.putText(image, str(self.currCounter), (640 - self.location_tup[0] + 25, self.location_tup[1] - 25), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0),2, cv2.LINE_AA)
            image = cv2.flip(image, 1)
            return image
        elif self.time_tup[0] < time < self.time_tup[1]:
            self.hittable = True
            
            image = cv2.rectangle(image, self.location_tup, [x -100 for x in self.location_tup], (0,0,255), -1)
            image = cv2.flip(image, 1)
            image = cv2.putText(image, str(self.currCounter), (640 - self.location_tup[0] + 25 , self.location_tup[1] - 25), cv2.FONT_HERSHEY_SIMPLEX, 2, (0,0,0), 2, cv2.LINE_AA)
            image = cv2.flip(image, 1)
            return image
        else:
            self.hittable = False
            return image


    def __str__(self):
        return f"{self.time_tup} location:{self.location_tup},type: {self.type}"

        
if __name__ == "__main__":
    s = OsuScheduler("./sasageyo.txt")
    print(s.data)
    # for hit in iter(s):
    #     print(hit)


