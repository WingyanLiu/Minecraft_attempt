
class Hero():
  def __init__(self,pos,land):
    self.land = land
    self.landfile = "land2.txt"
    self.hero = loader.loadModel('smiley')
    self.hero.setColor(1, 0.5, 0)
    self.hero.setScale(0.3)
    self.hero.setPos(pos)
    self.hero.reparentTo(render)
    self.game_mode = True
    self.cameraBind()
    self.accept_events()
    

  def cameraBind(self):
    base.disableMouse()
    base.camera.setH(180)
    base.camera.reparentTo(self.hero)
    base.camera.setPos(0, 0, 1.5)
    self.cameraOn = True

  def cameraUp(self):
    pos = self.hero.getPos()
    base.mouseInterfaceNode.setPos(-pos[0], -pos[1], -pos[2]-3)
    base.camera.reparentTo(render)
    base.enableMouse()
    self.cameraOn = False
  
  
  def accept_events(self):
    base.accept('с', self.changeView)
    def action_and_repeat(action_key,function):
      base.accept(action_key, function)
      base.accept(action_key+'-repeat', function)
      
    action_and_repeat('n',self.turn_left)
    action_and_repeat('m',self.turn_right)
    action_and_repeat('w',self.forward)
    action_and_repeat('s',self.back)
    action_and_repeat('a',self.left)
    action_and_repeat('d',self.right)
    action_and_repeat('h',self.turn_up)
    action_and_repeat('b',self.turn_down)
    base.accept('i', self.changeMode)
    base.accept( 'k', self.land.saveMap )
    base.accept( 'l', self.land.loadMap )
    base.accept('1', self.land.texture_brick)
    base.accept('2',self.land.texture_stone)
    base.accept('3',self.land.texture_wood)
    base.accept('0',self.land.texture_block)


    if self.game_mode == False:
      action_and_repeat('e',self.upward)
      action_and_repeat('f',self.downward)
    
    base.accept('b', self.build)
    base.accept('v', self.destroy)


  def changeMode(self):
    if self.game_mode == True:
      self.game_mode = False
      self.accept_events()
    else:
      self.game_mode = True
      self.accept_events()

  def changeView(self):
    if self.cameraOn:
      self.cameraUp()
    else:
      self.cameraBind()
  
  def check_dir(self, angle):
    if angle >= 0 and angle <= 20:
      return 0, -1
    elif angle >20 and angle <= 65:
      return 1, -1
    elif angle > 65 and angle <= 110:
      return 1,0
    elif angle >110 and angle <=155:
      return 1,1
    elif angle >155 and angle <= 200:
      return 0,1
    elif angle > 200 and angle <= 245:
      return -1,1
    elif angle > 245 and angle <= 290:
      return -1,0
    elif angle > 290 and angle <= 335:
      return -1,-1
    elif angle > 335 and angle < 360:
      return 0,-1

  def turn_left(self):
    self.hero.setH((self.hero.getH() + 5) % 360)

  def turn_right(self):
    self.hero.setH((self.hero.getH()-5)%360)
  
  def turn_up(self):
    if self.hero.getP()>=-90:
      self.hero.setP((self.hero.getP()-5))

  def turn_down(self):
    if self.hero.getP()<=90:
      self.hero.setP((self.hero.getP()+5))
  
  def just_move(self, angle):
    pos = self.look_at(angle)
    self.hero.setPos(pos)
  
  def try_move(self, angle):
    pos = self.look_at(angle)
    next_pos_z = self.land.height_at_this_pos(self.landfile, round(pos[0]),round(pos[1]))
    difference_in_z_pos = next_pos_z - (self.hero.getZ()-1) #-1 bc the hero is on top of the block and here we just want to consider the block it's on relative to other blocks
    if difference_in_z_pos > 0:
      if difference_in_z_pos == 1:
        #move up one z
        self.hero.setPos((pos[0],pos[1],next_pos_z+1))
        
      elif difference_in_z_pos >1:
        #cant move
        pass

    elif difference_in_z_pos < 0:
      # go down to the z_pos of that map correspondingly
      self.hero.setPos((pos[0],pos[1],next_pos_z+1))
    elif difference_in_z_pos == 0:
      #no need to change z_pos
      self.hero.setPos((pos[0],pos[1],next_pos_z+1)) #im checking here

    '''also, need to do a try catch for when the player try to walk
    out of map''' 


  def move_to(self, angle):
    pass

  def look_at(self, angle):
    from_x = round(self.hero.getX())
    from_y = round(self.hero.getY())
    from_z = round(self.hero.getZ())
    dx, dy  = self.check_dir(angle)
    return from_x + dx,from_y + dy, from_z
  
  def forward(self):
    angle =(self.hero.getH()) % 360
    if self.game_mode == True:
      self.try_move(angle)
    else:
      self.just_move(angle)

  def back(self):
    angle =(self.hero.getH()+180) % 360
    if self.game_mode == True:
      self.try_move(angle)
    else:
      self.just_move(angle)

  def left(self):
    angle =(self.hero.getH()+90) % 360
    if self.game_mode == True:
      self.try_move(angle)
    else:
      self.just_move(angle)

  def right(self):
    angle =(self.hero.getH()-90) % 360
    if self.game_mode == True:
      self.try_move(angle)
    else:
      self.just_move(angle)
  
  def upward(self):
    self.hero.setZ(self.hero.getZ() + 1) 
    print('upward() ran')
  
  def downward(self):
    self.hero.setZ(self.hero.getZ() - 1) 

  def build(self):
    angle = self.hero.getH() % 360
    pos = self.look_at(angle)
    if self.game_mode == False:
      self.land.addBlock(pos)
    else:
      self.land.buildBlock(pos)
  
  def destroy(self):
    angle = self.hero.getH() % 360
    pos = self.look_at(angle)
    if self.game_mode == False:
      self.land.delBlock(pos)
    else:
      self.land.delBlockFrom(pos)

  