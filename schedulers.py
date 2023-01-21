import cv2
import mediapipe as mp
import random

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
    def __init__(self,time_tup,location_tup,type="circle") -> None:
            self.time_tup = time_tup
            self.location_tup = location_tup
            self.type = type
    def isShown(self,time):
        return self.time_tup[0] <= time <= self.time_tup[1]

    def apply(image):
        ...

    def __str__(self):
        return f"{self.time_tup} location:{self.location_tup},type: {self.type}"

        
if __name__ == "__main__":
    s = RandomScheduler(2,70)
    for hit in iter(s):
        print(hit)


