class Scoreboard:
    def __init__(self, score, multiplier):
        self.score = score
        self.multiplier = multiplier
    def addScore(self, add): #adds score accounting for multiplier
        self.score += add * self.multiplier
    def resetScore(self):
        self.score = 0
    def resetMultiplier(self):
        self.multiplier = 1
    def setMultiplier(self, mult):
        self.multiplier = mult
    def getScore(self):
        return self.score
    def getMultiplier(self):
        return self.multiplier
    