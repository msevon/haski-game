from PyQt5 import QtGui, QtCore, QtWidgets
import os

from utils import paintBackground, saveScore, loadScore, clearScoreData, SoundPlayer, openMainMenu
from levelRenderer import LevelRenderer
from constantVariables import screenWidth, screenHeight, black, fade, green, yellow, red, turquoise, menuBackgroundSprite, menuMusic, saveFile
from levelRenderer import LevelRenderer
from exceptions import CorruptedLevelError

class MainMenu(): #class for main menu

    def __init__(self, scene): #creates the scene
        self.scene = scene    

    def openMainMenu(self): #opens the main menu
        #clear the scene and set own backgroung
        self.scene.clear()
        paintBackground(self.scene, menuBackgroundSprite)

        #create game title
        self.levelSelectionText = MenuText("Haski", screenWidth/2, screenHeight/2-100, black, 60)

        #create levelButtons
        self.playButton = MenuOption("Play", screenWidth/2, screenHeight/2-30, self, 28, black, None, 5)
        self.highScoreButton = MenuOption("Highscores", screenWidth/2, screenHeight/2+15, self, 28, black, None, 6)
        self.controlsMenuButton = MenuOption("Controls", screenWidth/2, screenHeight/2+60, self, 28, black, None, 8)
        self.exitButton = MenuOption("Exit", screenWidth/2, screenHeight/2+105, self.scene, 28, black, None, 2)

        #add title to scene
        self.scene.addItem(self.levelSelectionText)

        #add levelButtons to scene
        self.scene.addItem(self.playButton)
        self.scene.addItem(self.highScoreButton)
        self.scene.addItem(self.controlsMenuButton)
        self.scene.addItem(self.exitButton)

        #set menu music
        self.musicplayer = SoundPlayer()
        self.musicplayer.play(menuMusic)
        self.musicplaying = True

    def openLevelSelectionMenu(self): #opens the map selection menu
        #clear the scene and set own backgroung
        self.scene.clear()
        paintBackground(self.scene, menuBackgroundSprite)

        #if menu music is not playing, play it
        if self.musicplaying == False:
            self.musicplayer.play(menuMusic)

        #create menu title
        self.levelSelectionText = MenuText("Select level", screenWidth / 2, screenHeight / 2 - 170, black, 60)

        #call the map renderer
        renderer = LevelRenderer()

        #set the y position of the first levelButton
        y = -90

        #get files from the map directory
        for filename in os.listdir("levels/"):
            #check if file is valid type
            if filename.endswith(".txt"):
                try:

                    #load the level
                    level = renderer.renderLevel("levels/" + filename)

                    #create button for the level
                    levelButton = MenuOption(level.name, screenWidth / 2, screenHeight / 2 + y, self.scene, 28, black, level, 0)
                    y += 28

                    #create text showing the difficulty of the map
                    difficultyText = MenuText(level.difficulty, screenWidth / 2, screenHeight / 2 + y, black, 20)
                    
                    #add the items to the scene
                    self.scene.addItem(levelButton)
                    self.scene.addItem(difficultyText)

                    #set y position lower for the next levelButton
                    y += 45

                except CorruptedLevelError:
                    #if map file is corrupted it cannot be loaded
                    continue
            else:
                continue
        
        y += 10
        #create "back" levelButton
        self.backButton = MenuOption("Back to main menu", screenWidth / 2, screenHeight / 2 + y, self.scene, 28, black, None, 3)
        
        #add the title and the back levelButton to the scene
        self.scene.addItem(self.levelSelectionText)
        self.scene.addItem(self.backButton)

    def openControlsMenu(self): #opens the control menu
        #clear the scene
        self.scene.clear()

        #create text objects
        self.controlsText = MenuText("Controls", screenWidth/2, screenHeight/2-165, black, 60)
        self.movementText = MenuText("Movement: Arrow keys", screenWidth/2, screenHeight/2-70, black, 25)
        self.jumpText = MenuText("Jump: Spacebar", screenWidth/2, screenHeight/2-25, black, 25)
        self.pauseText = MenuText("Pause/resume: P", screenWidth/2, screenHeight/2 + 20, black, 25)
        self.retryText = MenuText("Retry: R", screenWidth/2, screenHeight/2+65, black, 25)
        self.menuText = MenuText("Menu: M", screenWidth/2, screenHeight/2+110, black, 25)

        #create back button
        self.backButton = MenuOption("Back to main menu", screenWidth / 2, screenHeight / 2 + 200, self.scene, 28, black, None, 3)

        #add items to the scene
        self.scene.addItem(self.controlsText)
        self.scene.addItem(self.movementText)
        self.scene.addItem(self.pauseText)
        self.scene.addItem(self.jumpText)
        self.scene.addItem(self.retryText)
        self.scene.addItem(self.menuText)
        self.scene.addItem(self.backButton)

    def openHighScoreMenu(self): #menu showing high scores for each level
        #clear the scene and paint the background
        self.scene.clear()
        paintBackground(self.scene, menuBackgroundSprite)

        #create title text
        self.highScoreText = MenuText("Highscores", screenWidth/2-300, screenHeight/2-225, black, 60)
        self.scene.addItem(self.highScoreText)
        y = -190
        for filename in os.listdir("levels/"):
            levelName = filename.strip(".txt")

            #get the level score
            levelScore = loadScore(levelName)

            #create title with level name
            self.levelNameText = MenuText(levelName, screenWidth / 2, screenHeight / 2 + y, black, 28)
            self.scene.addItem(self.levelNameText)
            y += 34
            if levelScore != False:
                #create text showing highscore for the level 
                score = levelScore[0]
                time = levelScore[1]
                self.levelTimeText = MenuText("Time left: " + str(time) + "s", screenWidth / 2, screenHeight / 2 + y, black, 20)
                y += 24
                self.levelDrunkText = MenuText("Drunkness: " + str(score) + "‰", screenWidth / 2, screenHeight / 2 + y, black, 20)
                self.scene.addItem(self.levelTimeText)
                self.scene.addItem(self.levelDrunkText)
            else:
                #if there isn't highscore yet for the level
                self.noHighScoreText = MenuText("No highscore yet...", screenWidth / 2, screenHeight / 2 + 15 + y, black, 20)
                self.scene.addItem(self.noHighScoreText)
                y += 24
            y += 50

        #create "back" and "clear data" button and add them to scene
        self.backButton = MenuOption("Back to main menu", screenWidth / 2 - 300, screenHeight / 2 + 210, self.scene, 28, black, None, 3)
        self.clearDataButton = MenuOption("Clear highscores", screenWidth / 2 + 300, screenHeight / 2 + 210, self, 28, black, None, 7)
        self.scene.addItem(self.backButton)
        self.scene.addItem(self.clearDataButton)


class PauseMenu(): #class for the pause menu object

    def __init__(self, scene): #initializes scene and creates variable for "paused" which upon creation is false
        self.scene = scene
        self.open = False
    
    def openPauseMenu(self): #opens pause menu
        #create title and the levelButtons
        self.MENU_TITLE = MenuText("Paused", screenWidth/2, screenHeight/2-100, black, 60)
        self.RESUME_levelButton = MenuOption("Resume", screenWidth/2, screenHeight/2-30, self.scene, 28, black, None, 4)
        self.mainMenu_levelButton = MenuOption("Main Menu", screenWidth/2, screenHeight/2+15, self.scene, 28, black, None, 3)

        #add controls to be shown
        self.movementText = MenuText("Movement: Arrow keys", screenWidth/2, screenHeight/2+120, black, 15)
        self.pauseText = MenuText("Pause and resume the game: P", screenWidth/2, screenHeight/2+145, black, 15)
        self.jumpText = MenuText("Jump: Spacebar", screenWidth/2, screenHeight/2+170, black, 15)
        self.retryText = MenuText("Retry: R", screenWidth/2, screenHeight/2+195, black, 15)
        
        

        #creates layer on top of the screen which fades the screen a little
        self.BACKGROUND = QtWidgets.QGraphicsRectItem(0, 0, screenWidth, screenHeight)
        self.BACKGROUND.setBrush(fade)

        #add the items to scene
        self.scene.addItem(self.BACKGROUND)
        self.scene.addItem(self.MENU_TITLE)
        self.scene.addItem(self.RESUME_levelButton)
        self.scene.addItem(self.mainMenu_levelButton)
        self.scene.addItem(self.movementText)
        self.scene.addItem(self.pauseText)
        self.scene.addItem(self.jumpText)
        self.scene.addItem(self.retryText)

        #set paused on True
        self.open = True

    def closePauseMenu(self): #closes pause menu
        #removes the pause menu items from scene
        self.scene.removeItem(self.MENU_TITLE)
        self.scene.removeItem(self.RESUME_levelButton)
        self.scene.removeItem(self.mainMenu_levelButton)
        self.scene.removeItem(self.BACKGROUND)
        self.scene.removeItem(self.movementText)
        self.scene.removeItem(self.pauseText)
        self.scene.removeItem(self.jumpText)
        self.scene.removeItem(self.retryText)


        #set paused on False
        self.open = False


class VictoryMenu(): #class for the menu object shown when player wins

    def __init__(self, scene): #initializes scene and sets "won" on False
        self.scene = scene
        self.open = False

    def closeVictoryMenu(self): #closes the victory menu
        #remove the win menu items from the scene 
        self.scene.removeItem(self.victoryTitle)
        self.scene.removeItem(self.retrylevelButton)
        self.scene.removeItem(self.mainMenulevelButton)
        self.scene.removeItem(self.beerText)
        self.scene.removeItem(self.timeText)
        self.scene.removeItem(self.background)

        #set open on false
        self.open = False
    
    def openVictoryMenu(self, points, time): #opens victory menu
        #create title, levelButtons, score and time 
        self.victoryTitle = MenuText("VICTORY!", screenWidth/2, screenHeight/2-100, yellow, 60)
        self.retrylevelButton = MenuOption("Select different map", screenWidth/2, screenHeight/2-30, self.scene, 28, black, self.scene.game, 1)
        self.mainMenulevelButton = MenuOption("Main Menu", screenWidth/2, screenHeight/2+15, self.scene, 28, black, None, 3)
        self.beerText = MenuText("Drunkness: {}‰".format(points), screenWidth/2+150, screenHeight/2+120, yellow, 28)
        self.timeText = MenuText("Time remaining: {}s".format(time), screenWidth / 2-150, screenHeight/2+120, yellow, 28)

        saveScore(self.scene.game.name, time, points)
        #creates layer on top of the screen which fades the screen a little
        self.background = QtWidgets.QGraphicsRectItem(0, 0, screenWidth, screenHeight)
        self.background.setBrush(fade)
        
        #add the items to scene
        self.scene.addItem(self.background)
        self.scene.addItem(self.victoryTitle)
        self.scene.addItem(self.retrylevelButton)
        self.scene.addItem(self.mainMenulevelButton)
        self.scene.addItem(self.beerText)
        self.scene.addItem(self.timeText)

        #set "won" on True
        self.open = True


class DeathMenu(): #class for the menu shown when player dies

    def __init__(self, scene):
        #create new scene
        self.scene = scene
        self.open = False

    def openDeathMenu(self): #adds the items to dead menu
        filename = self.scene.game.name + ".txt"
        renderer = LevelRenderer()
        level = renderer.renderLevel("levels/" + filename)
        self.menuTitle = MenuText("YOU ARE DEAD!!!", screenWidth / 2, screenHeight / 2 - 100, red, 60)
        self.tryAgain = MenuOption("Try again", screenWidth / 2, screenHeight / 2 - 30, self.scene, 28, black, level, 0)
        self.differentMap = MenuOption("Choose a different map", screenWidth / 2, screenHeight / 2 + 15, self.scene, 28, black, None, 1)
        self.mainMenu_levelButton = MenuOption("Main menu", screenWidth / 2, screenHeight / 2 + 60, self.scene, 28, black, None, 3)
        self.BACKGROUND = QtWidgets.QGraphicsRectItem(0, 0, screenWidth, screenHeight)
        self.BACKGROUND.setBrush(fade)
        self.scene.addItem(self.BACKGROUND)
        self.scene.addItem(self.menuTitle)
        self.scene.addItem(self.tryAgain)
        self.scene.addItem(self.differentMap)
        self.scene.addItem(self.mainMenu_levelButton)

    def closeDeathMenu(self): #removes all the items from dead menu
        self.scene.removeItem(self.menuTitle)
        self.scene.removeItem(self.tryAgain)
        self.scene.removeItem(self.differentMap)
        self.scene.removeItem(self.mainMenu_levelButton)
        self.scene.removeItem(self.BACKGROUND)


class MenuOption(QtWidgets.QGraphicsTextItem): #class for the option levelButtons used in different menus

    def __init__(self, text, x, y, scene, size, color, game, action):
        #initialize and set the position of levelButton
        super().__init__()
        self.text = text
        self.action = action
        self.x = x
        self.y = y
        self.size = size
        self.game = game
        self.writeText(color)
        self.scene = scene
        self.setPos(self.x - self.boundingRect().width() / 2, self.y - self.boundingRect().height() / 2)

    def hoverEnterEvent(self, e): #changes the way text looks when hovering over it
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.PointingHandCursor)
        self.writeText(turquoise)

    def hoverLeaveEvent(self, e): #changes the way text looks when hovering over it
        QtWidgets.QApplication.restoreOverrideCursor()
        self.writeText(black)

    def mousePressEvent(self, e): #handles the pressing of levelButton and does the action that is set for the levelButton
        action = self.action
        if action == 0: #displays the game
            self.scene.displayGame(self.game)
        elif action == 1: #displays the map selection menu
            self.scene.mainMenu.openLevelSelectionMenu()
        elif action == 2: #exits the game
            QtWidgets.QApplication.exit()
        elif action == 3: #displays main menu
            openMainMenu(self.scene)
        elif action == 4: #resumes game from pause
            self.scene.resumeGame()
        elif action == 5: #opens level selection menu
            self.scene.openLevelSelectionMenu()
        elif action == 6: #opens high score menu
            self.scene.openHighScoreMenu()
        elif action == 7: #clears highscoredata
            clearScoreData(saveFile)
            self.scene.openHighScoreMenu()
        elif action == 8:
            self.scene.openControlsMenu()

    def writeText(self, color):
        #creates the levelButton title
        self.setHtml("<p style='color:{};font-size:{}px;font-family:Impact;'>{}</p>".format(color, self.size, self.text))

class MenuText(QtWidgets.QGraphicsTextItem): #class used for the menu text

    def __init__(self, text, x, y, color, size):
        #initialize and set position of text
        super().__init__()
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.writeText(color, size)
        self.setPos(self.x - self.boundingRect().width() / 2, self.y - self.boundingRect().height() / 2)
    
    def writeText(self, color, size):
        #draws the text
        self.setHtml("<p style='color:{};font-size:{}px;font-family:Impact;'>{}</p>".format(color, size, self.text))