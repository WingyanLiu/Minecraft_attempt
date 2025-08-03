#write here code for creation and controlling map
from direct.showbase.ShowBase import ShowBase
import pickle

class Mapmanager():
    def __init__(self):
        self.model = 'block.egg' # the cube model is in block.egg file
        self.texture = 'block.png' # cube texture 
        self.landfile = 'land2.txt'          
        self.color = (1, 0.984, 0, 1) #rgba
        self.startNew()
        self.addBlock((0,10, 0))
        self.max_color = (0, 1, 0.05, 1)
        self.min_color = (0, 0.2, 0.05,1)
        

    def startNew(self):
        self.land = render.attachNewNode("Land")

    def addBlock(self,position):
        self.block = loader.loadModel(self.model)
        self.block.setTexture(loader.loadTexture(self.texture)) 
        self.block.setPos(position)
        self.block.setColor(self.color)
        self.block.reparentTo(self.land)
        x,y,z=position
        self.block.setTag("at", f"{x},{y},{z}")
        
        print('ran addBlock')
    
    def clear(self):
        self.land.removeNode()
        self.startNew()

    def isEmpty(self, pos):
        blocks = self.findBlocks(pos)
        if blocks:
            return False
        else:
            return True
    
    def findBlocks(self,pos):
        x,y,z = pos
        return self.land.findAllMatches(f"=at={x},{y},{z}")
    
    def findHighestEmpty(self,pos):
        x, y, z = pos
        z = 1
        while not self.isEmpty((x, y, z)):
            z += 1
        return (x, y, z)

    
    def buildBlock(self,pos):
        x, y, z = pos
        new = self.findHighestEmpty(pos)
        if new[2] <= z + 1:
            self.addBlock(new)
            self.modify_map(self.landfile,new,'add')



    def delBlock(self,position):
        blocks = self.findBlocks(position)
        
        for block in blocks:
            block.removeNode()
            
        self.modify_map(self.landfile,position,'del')


    def delBlockFrom(self,position):
        x, y, z = self.findHighestEmpty(position)
        pos = (x, y, z-1)
        blocks = self.findBlocks(pos)
        
        for block in blocks:
            block.removeNode()

        self.modify_map(self.landfile,pos,'del')

    def color_scale(self,land_file):
        max_height = 0
        with open(land_file) as file:
            lines = file.readlines()
            for line in lines:
                line = line.split(' ')
                for number in line:
                    if int(number) > max_height:
                        max_height = int(number)
        color_step = (self.max_color[1] - self.min_color[1])/max_height
        return color_step
                    
    def loadLand(self,land_file):
        color_step = self.color_scale(land_file)
        with open(land_file) as file:
            lines = file.readlines()
            y = 0
            for line in lines:
                x = 0
                line = line.split(' ')
                for z in line:
                    for z0 in range(int(z)+1):
                        block = self.addBlock((x, y, z0))
                        self.color = (1, self.min_color[1]+color_step*z0, 0, 1)
                    x += 1
                y += 1
        return x,y
    
    def height_at_this_pos(self,land_file,x,y):
        with open(land_file) as file:
            lines = file.readlines()
            line = lines[y].split(' ')
            z = line[x]
            return int(z)
    
    def modify_map(self,land_file,pos,action):
        x,y,z= pos
        print('pos: ',pos)
        print('z: ',z)


        with open(land_file) as file:
            lines = file.readlines()
            readedz = lines[y].split(' ')[x]
            modified_line = lines[y].split(' ')

            if action == 'add':
                modified_line[x]= str(z)
                
            if action == 'del':
                modified_line[x] = str(int(readedz)-1)
            
            #making it back to a single string
            modified_line = ' '.join(modified_line)

            lines[y] = modified_line

            txt = ''.join(lines)
        
        with open(land_file,'w') as file:
            file.write(txt)

    def saveMap(self):
        blocks = self.land.getChildren()
        with open('my_map.dat', 'wb') as fout:
            pickle.dump(len(blocks), fout)
            for block in blocks:
                x, y, z = block.getPos()
                pos = (int(x), int(y), int(z))
                pickle.dump(pos, fout)
    
    def loadMap(self):
        self.clear()
        with open('my_map.dat', 'rb') as fin:
            length = pickle.load(fin)
            for i in range(length):
                pos = pickle.load(fin)
                self.addBlock(pos)
    
    def texture_brick(self):
        self.texture = 'brick.png'
    
    def texture_stone(self):
        self.texture = 'stone.png'
    
    def texture_wood(self):
        self.texture = 'wood.png'
    
    def texture_block(self):
        self.texture = 'block.png'
