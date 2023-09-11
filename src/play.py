import sys

from gui import GUI

from PyQt5.QtWidgets import QApplication

#RUN THIS CODE TO PLAY THE GAME

def play(): #function to play the game
    global app
    app = QApplication(sys.argv)
    window = GUI()
    sys.exit(app.exec_())


play()
