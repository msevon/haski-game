from resources.item import Item
from constantVariables import stoneSprite
from utils import paint

from PyQt5 import QtWidgets

class Stone(Item): #class for the rock object

    def __init__(self, x, y, first_x, first_y, width, height):
        #initialize and paint the rock
        super().__init__(x, y, first_x, first_y, width, height)
        paint(self, stoneSprite)
