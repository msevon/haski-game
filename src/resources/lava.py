from resources.item import Item
from constantVariables import lavaSprite
from utils import paint


class Lava(Item): #class for the lava object

    def __init__(self, x, y, first_x, first_y, width, height):
        #initialize and paint the lava
        super().__init__(x, y, first_x, first_y, width, height)
        paint(self, lavaSprite)
