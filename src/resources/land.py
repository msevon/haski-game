from resources.item import Item
from constantVariables import landSprite
from utils import paint

from PyQt5 import QtWidgets

class Land(Item): #class for the ground object

    def __init__(self, x, y, first_x, first_y, width, height):
        super().__init__(x, y, first_x, first_y, width, height)
        paint(self,landSprite)
