from constantVariables import beerSprite
from utils import paint

from PyQt5 import QtWidgets, QtGui

class Beer(QtWidgets.QGraphicsEllipseItem): #class for the beer object

    def __init__(self, x, y, width, height, first_x, first_y,):
        #initialize, set position and paint the object
        super().__init__(x, y, width, height)
        self.x = first_x
        self.y = first_y
        self.setPos(self.x, self.y)
        paint(self,beerSprite)
        self.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0)))
        self.effect = QtWidgets.QGraphicsBlurEffect()