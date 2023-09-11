import unittest
from constantVariables import saveFile
from exceptions import CorruptedLevelError, CorruptedSaveFileError
from levelRenderer import LevelRenderer
from resources.haski import Haski
from resources.goal import Goal
from resources.cloud import Cloud
from utils import saveScore, clearScoreData,loadScore

class TestScores(unittest.TestCase): #tests for score saving, loading and overwriting

    def testSaveScore(self): #test saving score then loading it
        clearScoreData(saveFile)
        saveScore("Amsterdam",20,0.1)
        slot = loadScore("Amsterdam")
        self.assertEqual(slot[0],0.1)
        self.assertEqual(slot[1],20)
        clearScoreData(saveFile)

    def testOverWrite(self): #tests if saving a better score overwrites the old score
        clearScoreData(saveFile)
        saveScore("Siberia",30,1.0)
        saveScore("Siberia",40,1.5)
        slot = loadScore("Siberia")
        self.assertEqual(slot[0],1.5)
        self.assertEqual(slot[1],40)
        clearScoreData(saveFile)
    
    def testDeletedSaveFile(self):
        data=loadScore("Siberia")
        self.assertEqual(False, data)

class TestGenerateClouds(unittest.TestCase): #test generating clouds to level

    def setUp(self): #sets up tester
        self.levelRenderer = LevelRenderer()
        self.clouds = self.levelRenderer.generateClouds(1000)
        self.cloud = self.clouds[0]

    def testCloudType(self): #tests if index in clouds is type of Cloud
        self.assertEqual(type(self.cloud),Cloud)

    def testCloudDimensions(self): #tests the dimensions of cloud
        self.assertEqual(self.cloud.width, 470)
        self.assertEqual(self.cloud.height, 160)


class TestLevels(unittest.TestCase): #class used for testing map structure and information

    def setUp(self): #sets up tester
        self.game = None
        self.levelRenderer = LevelRenderer()
    
    #test all levels and their resources and info:

    def testLevel1(self):
        self.game = self.levelRenderer.renderLevel("levels/Amsterdam.txt")
        self.assertEqual("Amsterdam", self.game.name)
        self.assertEqual(50, self.game.time)
        self.assertEqual(2520, self.game.length)
        self.assertEqual(Haski, type(self.game.haski))
        self.assertEqual(Goal, type(self.game.goal))
        self.assertEqual(140, self.game.haski.x)
        self.assertEqual(2380, self.game.goal.x)
        self.assertEqual(31, len(self.game.lands))
        self.assertEqual(6, len(self.game.lavas))
        self.assertEqual(24, len(self.game.mushrooms))
        self.assertEqual(3, len(self.game.enemies))

    def testLevel2(self):
        self.game = self.levelRenderer.renderLevel("levels/Siberia.txt")
        self.assertEqual("Siberia", self.game.name)
        self.assertEqual(60, self.game.time)
        self.assertEqual(6230, self.game.length)
        self.assertEqual(Haski, type(self.game.haski))
        self.assertEqual(Goal, type(self.game.goal))
        self.assertEqual(140, self.game.haski.x)
        self.assertEqual(6090, self.game.goal.x)
        self.assertEqual(20, len(self.game.lands))
        self.assertEqual(19, len(self.game.lavas))
        self.assertEqual(127, len(self.game.mushrooms))
        self.assertEqual(10, len(self.game.enemies))

    def testLevel3(self):
        self.game = self.levelRenderer.renderLevel("levels/Turku.txt")
        self.assertEqual("Turku", self.game.name)
        self.assertEqual(70, self.game.time)
        self.assertEqual(7280, self.game.length)
        self.assertEqual(Haski, type(self.game.haski))
        self.assertEqual(Goal, type(self.game.goal))
        self.assertEqual(140, self.game.haski.x)
        self.assertEqual(7000, self.game.goal.x)
        self.assertEqual(75, len(self.game.lands))
        self.assertEqual(25, len(self.game.lavas))
        self.assertEqual(27, len(self.game.mushrooms))
        self.assertEqual(12, len(self.game.enemies))

    def testLevel4(self):
        self.game = self.levelRenderer.renderLevel("levels/Ulaanbaatar.txt")
        self.assertEqual("Ulaanbaatar", self.game.name)
        self.assertEqual(120, self.game.time)
        self.assertEqual(14210, self.game.length)
        self.assertEqual(Haski, type(self.game.haski))
        self.assertEqual(Goal, type(self.game.goal))
        self.assertEqual(140, self.game.haski.x)
        self.assertEqual(13720, self.game.goal.x)
        self.assertEqual(91, len(self.game.lands))
        self.assertEqual(118, len(self.game.lavas))
        self.assertEqual(170, len(self.game.mushrooms))
        self.assertEqual(64, len(self.game.enemies))

    #next 3 tests test if rendering an corrupted map raises CorruptedLevelError
    def testCorruptedLevel1(self): #level file has uneven map structure
        error = None
        try:
            self.levelRenderer.renderLevel("corruptlevels/corrupt.txt")
        except CorruptedLevelError:
            error = CorruptedLevelError
            self.assertEqual(error,CorruptedLevelError)

    def testCorruptedLevel2(self): #level has negative time
        error = None
        try:
            self.levelRenderer.renderLevel("corruptlevels/corrupt2.txt")
        except CorruptedLevelError:
            error = CorruptedLevelError
            self.assertEqual(error,CorruptedLevelError)

    def testCorruptedLevel3(self): #level doesn't have a goal
        error = None
        try:
            self.levelRenderer.renderLevel("corruptlevels/corrupt3.txt")
        except CorruptedLevelError:
            error = CorruptedLevelError
            self.assertEqual(error,CorruptedLevelError)

if __name__ == '__main__':
    unittest.main()