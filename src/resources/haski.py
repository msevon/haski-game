from PyQt5 import QtWidgets

from utils import paint, effect, SoundPlayer, openDeathMenu
from constantVariables import left, right, screenHeight, huskySprites, jumpSound, deathSound, victorySound
from resources.item import Item
from resources.beer import Beer
from resources.cloud import Cloud
from resources.lava import Lava
from random import randint

class Haski(Item): #class for the player object

    def __init__(self, x, y, first_x, first_y, width, height, scene):
        #initialize and paint the player
        super().__init__(x, y, first_x, first_y, width, height)
        self.first_x = first_x
        self.first_y = first_y
        self.x_speed = 0
        self.y_speed = 0
        self.y_acceleration = 0.5
        self.altitude = first_y
        self.sprite = 1
        self.drunkness = 0
        self.in_air = True
        self.still = True
        self.won = False
        self.dead = False
        self.scene = scene
        self.timer = 0
        self.sound = SoundPlayer()
        paint(self,huskySprites[self.sprite])
   
    def jump(self): #makes the player jump
        if self.in_air == False:
            self.in_air = True

            #paint jumping sprite
            self.sprite = 3
            paint(self,huskySprites[self.sprite])

            #play jump sound
            self.sound.play(jumpSound)
            #set jump height
            self.y_speed = -15

    def run(self): #make the player run while not jumping
        if self.in_air == False and self.still == False:
            self.timer += 1
            if self.timer == 7:
                if self.sprite == 0:
                    self.sprite = 1
                if self.sprite == 1 or self.sprite == 3:
                    self.sprite = 2
                elif self.sprite == 2:
                    self.sprite = 1
                paint(self,huskySprites[self.sprite])
                self.timer = 0
        elif self.still == True:
            self.sprite = 0
            paint(self,huskySprites[self.sprite])


    def drunk(self): #makes the player go drunk by blurring all objects
        effect(self, self.drunkness)
        effect(self.scene.game.goal, self.drunkness)

        def helper(resources):
            for resource in resources:
                effect(resource, self.drunkness)

        helper(self.scene.game.mushrooms)
        helper(self.scene.game.beers)
        helper(self.scene.game.lands)
        helper(self.scene.game.lavas)
        helper(self.scene.game.clouds)
        helper(self.scene.game.mushrooms)
        helper(self.scene.game.enemies)
        

    def win(self):
        #play sound and set won to be True
        self.sound.play(victorySound)
        self.won = True
        
    def die(self): #kills the player
        self.drunkness = 0

        #play sound
        self.sound.play(deathSound)

        #show death menu and stop the timer
        openDeathMenu(self.scene)
        self.scene.timer.stop()

        #set dead to be true
        self.dead = True