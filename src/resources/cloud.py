from resources.item import Item
from utils import paint
from constantVariables import cloudSprite

class Cloud(Item): #class for the cloud objects

    def __init__(self, x, y, first_x, first_y, width, height):
        #initialize and paint the cloud
        super().__init__(x, y, first_x, first_y, width, height)
        paint(self, cloudSprite)
