import numpy as np

class Tile():
    char = '?'
    color = 0
    world = None
    _x = 0
    _y = 0

    def __init__(self, x, y, world):
        self.world = world
        self._x = x
        self._y = y
    
    @property
    def name(self):
        return type(self).__name__
    
    @property
    def x(self):
        return self._x
        
    @property
    def y(self):
        return self._y
        
    @property
    def tileid(self):
        return self.world._getTileID(self._x, self._y)
    
    @tileid.setter
    def tileid(self, id):
        self.world._setTileID(self._x, self._y, id)
        
    @property
    def tiledata(self):
        return self.world._getTileData(self._x, self._y)
    
    @tiledata.setter
    def tiledata(self, data):
        self.world._setTileData(self._x, self._y, data)
         
        
    def update(self):
        pass
    
    def onEntry(self, entity):
        return False
        
    def onOccupy(self, entity):
        pass
        
    def render(self):
        return self.char, self.color
   
   
class EmptyTile(Tile):
    char = ' '  
        
        
class Entity():
    world = None
    
    char = '?'
    x = 0
    y = 0
    
    def __init__(self, x, y, char='?'):
        self.char = char
        self.x = x
        self.y = y
        
    def _update(self,):
        # Update tile agent it standing on
        self.world.getTile(self.x, self.y).onOccupy(self)
        
    def update(self, actiondict={}):
        if not actiondict.get("move") is None:
            dx, dy = actiondict["move"]
            self.move(dx, dy)
        
    def move(self, dx, dy):
        self.moveAbs(self.x+dx, self.y+dy)
    
    def moveAbs(self, x, y):
        # Only move if onEntry returns true
        if self.world.getTile(x, y).onEntry( self ):
            self.x = x
            self.y = y
        

        
        
class World():
    width = 80
    height = 50
    
    def __init__(self, tileset={}, generator=lambda x, y: (0,0), size=None):
        self.tileset = tileset
        self.generator = generator
        
        if not size is None:
            self.width, self.height = size
        
        # Fill map
        self.entities = []
        self.avatar = None
        self.map = np.zeros((self.width, self.height), dtype=np.int32)
        self.mapdata = np.zeros((self.width, self.height), dtype=np.int32)

        # Fill in map
        for x in range(self.width):
          for y in range(self.height):
            id, data = generator(x,y)
            self.map[x,y] = id
            self.mapdata[x,y] = data
        
        
    def _getTileID(self, x, y):
        try:
            return self.map[x,y]
        except:
            return 0
            
    def _setTileID(self, x, y, id):
        self.map[x,y] = id 
        
    def _getTileData(self, x, y):
        try:
            return self.mapdata[x,y]
        except:
            return 0
    
    def _setTileData(self, x, y, data):
        self.mapdata[x,y] = data
            
            
    def getTile(self, x, y):
        return self.tileset.get(self._getTileID(x,y), EmptyTile)(x, y, self)
        
        
    def addEntity(self, entity):
        self.entities.append(entity)
        entity.world = self
        
    def createEntity(self, entityClass, x, y, *args, **kwargs):
        entity = entityClass(x, y, *args, **kwargs)
        self.addEntity(entity)
        return entity
        
    def update(self, actiondict={}):
        for y in range(self.height):
          for x in range(self.width):
            self.getTile(x,y).update()
            
        for entity in self.entities:
            entity._update()
            entity.update()
            
        if not self.avatar is None:
            self.avatar.update(actiondict)
    

    
        


