from constantVariables import screenWidth, screenHeight
from scene import Scene

from PyQt5 import QtWidgets

class GUI(QtWidgets.QMainWindow): #class for the gui object
    
    def __init__(self): #initializes the gui
        super().__init__()

        #set screen width and height to match the game
        self.width = screenWidth
        self.height = screenHeight

        #set the title of the window
        self.title = "Haski"
        self.setWindowTitle(self.title)

        #set the window dimensions
        self.x = 500
        self.y = 250

        #set the geometry of window
        self.setGeometry(self.x, self.y, self.width, self.height)

        #create the scene
        self.scene = Scene(self.width, self.height)

        #show the window
        self.show()

        #set mousetracking on
        self.setMouseTracking(True)

        #fix the size
        self.setFixedSize(self.width, self.height)

        #set the view
        self.setView()

    def setView(self): #sets the view
        self.view = QtWidgets.QGraphicsView(self.scene, self)

        #adjust the size of the view
        self.view.adjustSize()

        #show the view
        self.view.show()
