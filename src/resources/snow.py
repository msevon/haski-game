
from resources.item import Item
from constantVariables import snowSprite
from utils import paint

from PyQt5 import QtWidgets

class Snow(Item): #class for the snow object

    def __init__(self, x, y, first_x, first_y, width, height):
        #initialize and paint the snow object
        super().__init__(x, y, first_x, first_y, width, height)
        paint(self, snowSprite)
