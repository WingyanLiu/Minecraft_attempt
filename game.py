#write here a code for main window of the game
from direct.showbase.ShowBase import ShowBase
from mapmanager import Mapmanager
from hero import Hero

class Game(ShowBase):
    def __init__(self):
        ShowBase.__init__(self)
        self.land = Mapmanager() #create a map
        base.camLens.setFov(90)
        x,y = self.land.loadLand("land2.txt")
        self.hero = Hero(pos=(x//2,y//2,self.land.height_at_this_pos('land2.txt',x//2,y//2)+1),land = self.land) #to spawn the player in the middle of the map

game = Game()
game.run()

#Note: the color height thing aint working properly, fix it later.