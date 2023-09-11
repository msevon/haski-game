from PyQt5 import QtWidgets, QtGui, QtCore

#controls
space = QtCore.Qt.Key_Space
right = QtCore.Qt.Key_Right
left = QtCore.Qt.Key_Left
pauseMenu = QtCore.Qt.Key_P
retry = QtCore.Qt.Key_R
menu = QtCore.Qt.Key_M

#gameplay
screenWidth = 900
screenHeight = 550
timerSpeed = 15

#saving
saveFile = "saveFile.txt"

#sounds used in game
beerCollectSound = "sounds/beercollect.mp3"
jumpSound = "sounds/jump.mp3"
deathSound = "sounds/death.mp3"
victorySound = "sounds/victory.mp3"
menuMusic = "sounds/menumusic.mp3"

#sprites used in the game
huskySprites = ["sprites/huskyStill.png", "sprites/huskyWalk1","sprites/huskyWalk2","sprites/huskyJump"]
enemySprites = ["sprites/enemy1.png", "sprites/enemy2.png"]
beerSprite= "sprites/beer.png"
goalSprite = "sprites/goal.png"
cloudSprite = "sprites/cloud.png"
landSprite = "sprites/land.png"
mushroomSprite = "sprites/mushroom.png"
snowSprite = "sprites/snow.png"
stoneSprite = "sprites/stone.png"
lavaSprite = "sprites/lava.png"
levelBackground = "sprites/gameBackground.png"
menuBackgroundSprite = "sprites/gameBackground.png"

#colors and fade
red = "#ff0000"
turquoise = "#50fffc"
green = "#00ff00"
yellow = "#ffd700"
black = "#000000"
fade = QtGui.QColor(0, 0, 0, 150)

