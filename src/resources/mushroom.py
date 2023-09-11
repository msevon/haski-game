from PyQt5 import QtWidgets, QtGui

from utils import paint
from resources.item import Item
from constantVariables import mushroomSprite

class Mushroom(Item): #class for the mushroom platforms

    def __init__(self, x, y, first_x, first_y, width, height):
        #initialize and paint the object
        super().__init__(x, y, first_x, first_y, width, height)
        paint(self, mushroomSprite)
