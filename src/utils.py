from PyQt5 import QtGui, QtMultimedia, QtWidgets, QtCore
import os

from exceptions import CorruptedSaveFileError
from constantVariables import saveFile, menuMusic
from random import randint

#helper functions

def paint(obj,sprite):
    obj.setBrush(QtGui.QBrush(QtGui.QImage(sprite)))
    
def paintBackground(obj,sprite):
    obj.setBackgroundBrush(QtGui.QBrush(QtGui.QImage(sprite)))
    
def effect(obj, drunkness):
    obj.effect.setBlurRadius(drunkness*5)
    obj.setGraphicsEffect(obj.effect)

def saveScore(levelName, time, score): #saves the level score to local file
    try: #check if save file exists
        savefile = open(saveFile,"r")
        saveslots = savefile.readlines()
        savefile.close()

        #check if possible old saveslots need to be deleted
        overWrite = overwrite(saveslots, levelName, time, score)

        if overWrite == True:
            #rewrite file with new save slot
            savefile = open(saveFile,"w")
            for slot in saveslots:
                data = slot.split("/")
                if data[0] != levelName:
                    savefile.write(slot)
            savefile.write(levelName + "/" + str(time) + "/" + str(score))
            savefile.write("\n")
            savefile.close()
    except FileNotFoundError: #create save file
        savefile = open(saveFile,"w")
        savefile.write(levelName + "/" + str(time) + "/" + str(score))
        savefile.write("\n")
        savefile.close()


def overwrite(saveslots, levelName, time, score): #checks if saveslot already exists for level, returns True if new score is better, else returns False
    for slot in saveslots:
        data = slot.split("/")
        if data[0] == levelName:
            oldScore = data[2].strip("\n")
            oldScore = float(oldScore)
            oldTime = int(data[1])

            #compare old score and new score
            if oldScore > score:
                return False
            elif oldScore == score:
                #compare old time and new time
                if oldTime >= time:
                    return False
                else:
                    return True
            else:
                return True
    #no previous save
    return True

def loadScore(levelName):
    try:
        savefile = open(saveFile,"r")
        saveslots = savefile.readlines()
        savefile.close()
        for slot in saveslots:
            data = slot.split("/")
            if data[0] == levelName:
                oldScore = data[2].strip("\n")
                oldScore = float(oldScore)
                oldTime = int(data[1])
                return oldScore, oldTime
        return False 

    except FileNotFoundError:
        return False

def clearScoreData(sfile):
    if os.path.exists(sfile):
        os.remove(sfile)

#functions for opening and closing different menus # # # #
                                                         #
def openMainMenu(scene):                                 #
    scene.playing = False                                #                                  
    closeMenus(scene)                                    #
    scene.musicplayer.stop()                             #
    scene.mainMenu.musicplaying = False                  #
    scene.mainMenu.musicplayer.play(menuMusic)           #
    scene.mainMenu.openMainMenu()                        #
                                                         #
def openVictoryMenu(scene, drunkness, time):             #
    if not scene.victoryMenu.open:                       #
        scene.musicplayer.stop()                         #
        scene.mainMenu.musicplaying = False              #
        scene.victoryMenu.openVictoryMenu(round(drunkness,1),time)  
        scene.victoryMenu.open = True                    #
                                                         #
def closeVictoryMenu(scene):                             #
    if scene.victoryMenu.open:                           #
        scene.victoryMenu.closeVictoryMenu()             # 
        scene.victoryMenu.open = False                   #
                                                         #
def openPauseMenu(scene):                                #
    if not scene.pauseMenu.open:                         #                      
        scene.pauseMenu.openPauseMenu()                  #
        scene.pauseMenu.open = True                      #
                                                         #
def closePauseMenu(scene):                               #
    if scene.pauseMenu.open:                             #                    
        scene.pauseMenu.closePauseMenu()                 #
        scene.pauseMenu.open = False                     #
                                                         #
def openDeathMenu(scene):                                #
    if not scene.deathMenu.open:                         #
        scene.musicplayer.stop()                         #
        scene.mainMenu.musicplaying = False              #
        scene.deathMenu.openDeathMenu()                  #
        scene.deathMenu.open = True                      #
                                                         #
def closeDeathMenu(scene):                               #
    if scene.deathMenu.open:                             #
        scene.deathMenu.closeDeathMenu()                 #
        scene.deathMenu.open = False                     #
                                                         # 
                                                         #
 # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#closes all the game menus except main
def closeMenus(scene):
    scene.pauseMenu.open = False
    scene.deathMenu.open = False
    scene.victoryMenu.open = False



#helper classes

class SoundPlayer(QtWidgets.QGraphicsScene): #plays sounds used in the game

    def __init__(self):
        self.player = QtMultimedia.QMediaPlayer()

    def play(self,song):
        url = QtCore.QUrl.fromLocalFile(song)
        content = QtMultimedia.QMediaContent(url)
        self.player.setMedia(content)
        self.player.play()

    def stop(self):
        self.player.stop()