from PyQt5 import QtWidgets, QtGui, QtCore

from resources.land import Land
from resources.beer import Beer
from resources.goal import Goal
from resources.lava import Lava
from resources.mushroom import Mushroom
from resources.cloud import Cloud
from resources.enemy import Enemy
from resources.snow import Snow
from resources.stone import Stone

from utils import SoundPlayer, openVictoryMenu
from constantVariables import screenWidth, screenHeight, right, left, beerCollectSound

class Session(): #creates the game session object

    def __init__(self, name, time, music, difficulty, player, lands, mushrooms, clouds, beers, lavas, enemies, goal, length, scene): #initializes the game object
        #set name, time, music and difficulty
        self.name = name
        self.time = time
        self.music = music
        self.difficulty = difficulty

        #set the resources
        self.player = player
        self.lands = lands
        self.mushrooms = mushrooms
        self.clouds = clouds
        self.beers = beers
        self.lavas = lavas
        self.enemies = enemies
        self.goal = goal

        #set the length
        self.length = length

        #set the direction to be None
        self.direction = None

        #set paused on false
        self.paused = False
        
        #set offset of player
        self.offset = player.x

        #set the timer and update it
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateTime)

        #set the game scene
        self.scene = scene

    def updateTime(self): #updates the timer every second
        #take one second away and update the time text
        self.time -= 1
        self.scene.updateTime()

        #if time reaches 0, top the game and kill the player
        if self.time == 0:
            self.timer.stop()
            self.player.die()

    def start(self): #start the
        self.timer.start(1000) #1000ms = 1s

    def runGame(self): #runs the game cycle
        #update husky and enemy resources
        if self.player.in_air == False:
            self.player.run()
        for enemy in self.enemies:
            enemy.move()

        #if player wins or dies stop the game and scene timer
        if self.player.dead or self.player.won:
            self.scene.timer.stop()
            self.timer.stop()
        else:
            #if player is jumping set "in_air" to be true
            if self.player.y_speed != 0:
                self.player.in_air = True

            #adds the player jumping accelleration and velocity to the players y-coordinate
            self.player.y_speed += self.player.y_acceleration
            self.player.y += self.player.y_speed

            #if player falls out of screen kill the player
            if self.player.y >= screenHeight:
                self.player.die()

            else:
                #updates the players y-coordinate
                self.player.setY(self.player.y)

                #players new y position
                newY = 0

                #set dy as players jumping height
                dy = self.player.y_speed

                #search for obstacles in player's colliding items
                for obstacle in self.player.collidingItems():

                    #if the obstacle is ground, box, snow, rock or spike do this
                    if type(obstacle) in (Land, Mushroom, Snow, Stone, Lava):
                        
                        #if player != on the object or under it
                        if not (self.player.x + self.player.width == obstacle.x or self.player.x == obstacle.x + obstacle.width):
                            
                            #if player collides on the object
                            if dy > 0:
                                
                                #if the object is lava, kill the player
                                if type(obstacle) == Lava:
                                    self.player.die()

                                #else set the player on ground and set the new y on the ground
                                else:
                                    self.player.in_air = False
                                    newY = obstacle.y - self.player.height
                                    self.player.y_speed = 0
                            
                            #if player collides under the object set it's velocity to 1 and set new y under the object
                            elif dy < 0:
                                newY = obstacle.y + obstacle.height
                                self.player.y_speed = 1
                                break
                        #if the obstacle is coin, enemy or flag detect the hit
                    elif type(obstacle) in (Beer, Enemy, Goal):
                        self.collision(obstacle)

                #if player != on ground
                if newY != 0:
                    
                    #set the players y coordinate as the new y
                    self.player.y = newY
                    self.player.setY(self.player.y)

            if not self.player.dead: #if player is alive

                #if player is moving                
                if self.direction != None:
                    
                    #if the direction is left change the x-coordinate by +5
                    if self.direction == left:
                        dx = 5

                    #if the direction is left change the x-coordinate by -5
                    elif self.direction == right:
                        dx = -5
                    
                    #set the player's new coordinates according to the direction it's facing
                    self.player.x -= dx
                    self.player.setX(self.player.x)

                    #prevent the player from moving out of the window from right
                    if self.player.x > screenWidth - self.player.width:
                        self.player.x = screenWidth - self.player.width
                        self.player.setX(self.player.x)

                    #prevent the player from moving out of the window from left
                    elif self.player.x < 0:
                        self.player.x = 0
                        self.player.setX(self.player.x)

                    else:
                        #set new x-coordinate as the change of x
                        newX = dx

                        #search for obstacles in player's colliding items
                        for obstacle in self.player.collidingItems():

                            #if the obstacle is ground, box, snow, rock or spike do this
                            if type(obstacle) in (Land, Mushroom, Lava, Snow, Stone):
                                
                                #if player != at the same height as the object
                                if not (self.player.y + self.player.height == obstacle.y or self.player.y == obstacle.y + obstacle.height):
                                    
                                    #stop the player upon collision
                                    if dx > 0:
                                        newX = -(obstacle.x + obstacle.width - self.player.x - dx)

                                    elif dx < 0:
                                        newX = self.player.x + self.player.width - obstacle.x + dx
                                        
                                    break
                            
                            #if the obstacle is coin, enemy or flag detect the hit
                            elif type(obstacle) in (Beer, Enemy, Goal):
                                self.collision(obstacle)
                        
                        #change the offset by the new x-coordinate
                        self.offset -= newX

                        #if the offset is less than half of the screen the player moves and the scene stays still
                        if self.offset < 250 or self.offset > self.length - 750:
                            #move player back after checking for collisions
                            if newX == 0:
                                self.player.x += dx
                                self.player.setX(self.player.x)
                        else:

                            #if the offset is more than half of the screen the scene moves and the player stays still
                            self.player.x += dx
                            self.player.setX(self.player.x)

                            #move all the items
                            if newX != 0:
                                for lava in self.lavas:
                                    lava.x += newX
                                    lava.setX(lava.x)
                                for land in self.lands:
                                    land.x += newX
                                    land.setX(land.x)
                                for block in self.mushrooms:
                                    block.x += newX
                                    block.setX(block.x)
                                for beer in self.beers:
                                    beer.x += newX
                                    beer.setX(beer.x)
                                for enemy in self.enemies:
                                    enemy.x += newX
                                    enemy.setX(enemy.x)
                                self.goal.x += newX
                                self.goal.setX(self.goal.x)

                                #move clouds but 3x slower
                                for cloud in self.clouds:
                                    cloud.x += (newX / 3)
                                    cloud.setX(cloud.x)

            else: #if player dies
                #stop the timer
                self.timer.stop()

    def collision(self, obj): #function used for handling collisions with interactive items
        #when colliding with a beer make it disappear and gain +1 beers
        if type(obj) == Beer and obj.isVisible():
            self.player.drunkness += 0.1
            self.sound = SoundPlayer()
            self.sound.play(beerCollectSound)
            self.player.drunk()
            obj.setVisible(False)
            self.scene.updateDrunkness()

        #when colliding with an enemy kill the player and stop the timer
        elif type(obj) == Enemy:
            self.player.die()
            self.timer.stop()
        
        #when colliding with the goal open victory menu and make the player win
        elif type(obj) == Goal:
            openVictoryMenu(self.scene,self.player.drunkness, self.time)
            self.player.win()
