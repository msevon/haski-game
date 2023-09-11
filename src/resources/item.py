
from PyQt5 import QtWidgets, QtGui

class Item(QtWidgets.QGraphicsRectItem): #parent/base object for all the game's items

    def __init__(self, x, y, width, height, first_x, first_y):
        #initialize the object
        super().__init__(x, y, width, height)
        self.x = first_x
        self.y = first_y
        self.width = width
        self.height = height
        self.effect = QtWidgets.QGraphicsBlurEffect()

        #sets the position of the object
        self.setPos(first_x, first_y)

        #paints the object
        self.setPen(QtGui.QPen(QtGui.QColor(0, 0, 0, 0)))