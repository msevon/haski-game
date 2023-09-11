from exceptions import CorruptedLevelError
from session import Session
from random import randint
from resources.land import Land
from resources.beer import Beer
from resources.goal import Goal
from resources.lava import Lava
from resources.haski import Haski
from resources.mushroom import Mushroom
from resources.cloud import Cloud
from resources.enemy import Enemy
from resources.snow import Snow
from resources.stone import Stone

class LevelRenderer(): #reads the map file and renders it

    def renderLevel(self, path): #loads the map and returns complete game object
        #map info contains the title, time and the difficulty of the map
        self.levelInfo = {"title" : None, "time" : None, "music": None, "difficulty" : None}

        #map data contains all of the map resources and map length
        self.levelData = {
            "H": None, #haski
            "X" : None, #goal
            "G" : [], #land blocks
            "L" : [], #lava blocks
            "R" : [], #stone/rock blocks
            "S" : [], #snow blocks
            "B" : [], #beers
            "M" : [], #mushroom blocks
            "E" : [], #enemies
            "length" : 0 #map length
        }

        #initialize level data
        levelData = { '#info': [self.readLevelInfo,[]],'#level': [self.readLevelResources,[]] }
        try:
            #open the level file
            levelFile = open(path)
            line = None
            current = None
            while line != '':
                #read the line and split it
                line = levelFile.readline()
                chunk = line.strip().split( ' ' )
                chunk = ' '.join(chunk)
                chunk = chunk.lower()

                #if chunk contains levelInfo or levelResources
                if chunk in levelData:
                    current = chunk
                if current:
                    levelData[current][1].append(chunk)

            #calls the function readLevelInfo or readLevelResources
            for chunk in levelData:
                levelData[chunk][0](levelData[chunk][1])
        except IOError:
            raise CorruptedLevelError("Cannot find specified level file.")
        finally:
            #close the file
            levelFile.close()

        length = self.levelData["length"]
        clouds = self.generateClouds(length)
        time = self.levelInfo["time"]
        name = self.levelInfo["title"]
        music = self.levelInfo["music"]
        difficulty = self.levelInfo["difficulty"]
        haski = self.levelData["H"]
        lands = self.levelData["G"] + self.levelData["S"] #land and ice are the same
        mushrooms = self.levelData["M"] + self.levelData["R"] #Boxes and stones are the same
        lavas = self.levelData["L"] 
        beers = self.levelData["B"] 
        enemies = self.levelData["E"] 
        goal = self.levelData["X"]

        if (haski == None or goal == None):
            raise CorruptedLevelError("There is no player or goal in the level.")

        #create the game and return it
        game = Session(name, time, music, difficulty, haski, lands, mushrooms, clouds, beers, lavas, enemies, goal, length, None)
        return game

    def readLevelInfo(self,data):  #reads map info data
        #collect difficulty, title and time from data
        data = data[1:]
        data = list(filter(None, data))
        
        #if data length is 3, map isn't corrupted and is readable
        if len(data) == 4:
            for line in data:
                #splits current line's items
                items = line.split("=") 
                if items[0] in self.levelInfo:
                    #collect title value from the line
                    if items[0] == "title":
                        self.levelInfo[items[0]] = items[1].capitalize()
                    #collect time value from the line
                    elif items[0] == "time":
                        try:
                            if int(items[1]) >= 0:
                                self.levelInfo[items[0]] = int(items[1])
                            else:
                                raise CorruptedLevelError("Level time cannot be negative.")
                        except ValueError:
                            raise CorruptedLevelError("Time must be an integer.")
                    #collect music value from the line
                    elif items[0] == "music":
                        self.levelInfo[items[0]] = items[1]
                    #collect difficulty value from the line
                    elif items[0] == "difficulty":
                        self.levelInfo[items[0]] = items[1]
            #handle possible errors
                else:
                    raise CorruptedLevelError("Wrong variable in map data. Allowed variables: title, time, music or difficulty")
        else:
            raise CorruptedLevelError("Too manu variables in map data.")

    def readLevelResources(self,resources):
        #collect complete map file lines by eliminating empty strings
        resources = resources[1:]
        resources = list(filter(None, resources))

        #create variables for stage_length and y position
        levelLength = 0
        y = 0

        #create loop that goes through the whole map file
        for i, line in enumerate(resources):

            #create variable for the x position
            x = 0

            #split game resources form line
            line = line.rstrip().split(',')

            #go through all resources
            for column in line:
                column = column.capitalize()
                if column in self.levelData:
                    #create game resources based on column letters
                    if column == 'G': #if ground block
                        self.levelData[column].append(Land(0, 0, 70, 70, x, y))
                    elif column == 'R': #if stone block
                        self.levelData[column].append(Stone(0, 0, 70, 70, x, y))
                    elif column == 'M': #if mushroom block
                        self.levelData[column].append(Mushroom(0, 0, 70, 70, x, y))
                    elif column == 'S': #if snow block
                        self.levelData[column].append(Snow(0, 0, 70, 70, x, y))
                    elif column == 'B': #if beer
                        self.levelData[column].append(Beer(0, 0, 38, 38, x + 19, y + 19))
                    elif column == 'E': #if enemy
                        self.levelData[column].append(Enemy(0, 0, 53, 70, x, y))
                    elif column == 'L': #if lava
                        self.levelData[column].append(Lava(0, 0, 70, 35, x, y + 35))
                    elif column == 'H': #if haski
                        if self.levelData[column] is not None: #if there is two or more players
                            raise CorruptedLevelError("Level can only contain one player.")
                        else:
                            self.levelData[column] =  Haski(0, 0, 61, 130, x, y, None)
                    elif column == 'X': #if goal
                        if self.levelData[column] is not None: #if more than 1 goal
                            raise CorruptedLevelError("Level can only contain 1 goal.")
                        else:
                            self.levelData[column] = Goal(0, 0, 30, 90, x, y)
                x += 70
            #sets the level length as final x-coordinate of map
            if i == 0:
                levelLength = x
                self.levelData["length"] = x
            else:
                if x != levelLength:
                    raise CorruptedLevelError("Every line in the map file should have equal amount of resources.")
            y += 70

    def generateClouds(self, max): #generates clouds in the level
        clouds = []
        x = 0
        while x < max:
            y = randint(40, 70)
            cloud = Cloud(0, 0, 470, 160, x, y)
            clouds.append(cloud)
            random = randint(1000,2000)
            x += random

        return clouds



        