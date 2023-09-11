from resources.item import Item
from constantVariables import goalSprite
from utils import paint

from PyQt5 import QtGui

class Goal(Item): #class for the goal object

    def __init__(self, x, y, first_x, first_y, width, height):
        #initialize object and paint it
        super().__init__(x, y, first_x, first_y, width, height)
        paint(self, goalSprite)
