from PyQt5 import QtWidgets, QtCore, QtGui, QtMultimedia

from utils import paintBackground
from levelRenderer import LevelRenderer
from constantVariables import timerSpeed, left, right, space, retry, pauseMenu, menu, levelBackground, menuMusic
from utils import SoundPlayer, openMainMenu, openPauseMenu, closeMenus, closePauseMenu
from menus import PauseMenu, DeathMenu, VictoryMenu, MainMenu
from session import Session

class Scene(QtWidgets.QGraphicsScene): #creates the scene used in the game session

    def __init__(self, width, height): #create and initialize the scene
        super().__init__()

        #set the scene dimensions and view
        self.width = width
        self.height = height

        self.musicplayer = SoundPlayer()

        #creates rectangular scene
        self.setSceneRect(0, 0, width, height)

        #create all the menus
        self.mainMenu = MainMenu(self)
        self.victoryMenu = VictoryMenu(self)
        self.pauseMenu = PauseMenu(self)
        self.deathMenu = DeathMenu(self)

        #create the main menu
        self.mainMenu.openMainMenu()

        #initialize timer
        self.timer = QtCore.QBasicTimer()

        #set playing on false
        self.playing = False

        #set game still on none
        self.game = None

    def setView(self, view): #sets the view for the scene
        self.view = view

    def displayGame(self, game): #displays the game
        #clear the scene
        self.clear()

        #close all the menus
        closeMenus(self)

        #stop menu music
        self.mainMenu.musicplayer.stop()

        #draw the background
        paintBackground(self,levelBackground)

        #initialize the game
        self.game = game

        #initialize this scene for the player and the game
        self.game.player.scene = self
        self.game.scene = self

        #add the items to the map
        for cloud in self.game.clouds:
            self.addItem(cloud)
        for enemy in self.game.enemies:
            self.addItem(enemy)
        self.addItem(self.game.goal)
        self.addItem(self.game.player)
        for land in self.game.lands:
            self.addItem(land)
        for block in self.game.mushrooms:
            self.addItem(block)
        for lava in self.game.lavas:
            self.addItem(lava)
        for beer in self.game.beers:
            self.addItem(beer)

        #add the beers and time to be visible
        self.setTimer()
        self.setDrunkCounter()

        #start the timer
        self.timer.start(timerSpeed, self)

        #play the level music
        self.musicplayer.play(self.game.music)

        #set playing to be true and start the game
        self.playing = True
        self.game.start()

    def setTimer(self): #adds the time text item to scene
        self.time_text = QtWidgets.QGraphicsTextItem()

        #set the position of the text
        self.time_text.setPos(0, 10)

        #add the text item and update the time
        self.addItem(self.time_text)
        self.updateTime()

    def updateTime(self): #updates the time
        self.time_text.setHtml("<p style='color:yellow;font-size:20px;font-family:Impact;'>Time remaining: {}</p>".format(self.game.time))

    def timerEvent(self, e): #updates the game with time
        self.game.runGame()

    def setDrunkCounter(self): #adds the beer text item to the scene
        self.drunkText = QtWidgets.QGraphicsTextItem()

        #set the position for the text
        self.drunkText.setPos(750, 10)

        #add the text item and update beers
        self.addItem(self.drunkText)
        self.updateDrunkness()

    def updateDrunkness(self): #updates beer count
        self.drunkText.setHtml("<p style='color:yellow;font-size:20px;font-family:Impact;'>Drunkness: {}‰</p>".format(round(self.game.player.drunkness,1)))

    def resumeGame(self): #resumes the game
        #set paused on false
        self.game.paused = False

        #start the game and scene timers
        self.game.timer.start(1000)
        self.timer.start(timerSpeed, self)

        #close the pause menu
        closePauseMenu(self)
        
    def pauseGame(self): #pauses the game
        #set paused on true
        self.game.paused = True

        #stop the game and scene timers
        self.game.timer.stop()
        self.timer.stop()

        #open the pause menu
        openPauseMenu(self)

    def keyPressEvent(self, e): #handles the pressing of keys
        #initialize the key pressed
        key = e.key()
        if self.playing:
            
            #change the direction if pressed left or right
            if key in (left, right):
                self.game.player.still = False
                #self.game.player.run()
                self.game.direction = key

            #jump if pressed space
            if key == space:
                self.game.player.jump()

            #show pause menu and stop the game if pressed pause
            if key == pauseMenu and not self.game.player.dead:
                if self.game.paused:
                    self.resumeGame()
                else:
                    self.pauseGame()
            
            #retry current level
            if key == retry and self.playing == True:
                filename = self.game.name + ".txt"
                renderer = LevelRenderer()
                level = renderer.renderLevel("levels/" + filename)
                self.displayGame(level)
            
            #go back to main menu
            if key == menu and self.playing == True:
                self.pauseGame()
                openMainMenu(self)


    def keyReleaseEvent(self, e): #handles the release of keys
        #initialize the released key
        key = e.key()
        if self.playing:

            #if released left or right stop the player
            if key in (left, right):
                self.game.player.still = True
                self.game.direction = None
    
