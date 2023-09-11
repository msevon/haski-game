from resources.item import Item
from constantVariables import left, right, enemySprites
from random import randint
from utils import paint

from PyQt5 import QtWidgets

class Enemy(Item): #class for the enemy object

    def __init__(self, x, y, first_x, first_y, width, height):
        #initialize enemy and it's update clock
        super().__init__(x, y, first_x, first_y, width, height)
        paint(self,enemySprites[1])
        self.sprite = randint(0,1)
        self.enemy_timer = 0

    def move(self): #makes the enemy move
        #increase the timer count
        self.enemy_timer += 1

        #if timer reaches 20 change the sprite
        if self.enemy_timer == 20:
            if self.sprite == 0:
                self.sprite += 1
            else:
                self.sprite -= 1

            #paint the new sprite and set timer to 0
            paint(self, enemySprites[self.sprite])
            self.enemy_timer = 0
        
        
            