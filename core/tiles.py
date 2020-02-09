from .core import Tile

class SkyTile(Tile):
    color = 255
    
class GroundTile(Tile):
    char = '.'
    
    @property
    def color(self):
        return self.tiledata % 256
        
    def onEntry(self, entity):
        return True
        
    def onOccupy(self, entity):
        self.tiledata = max(0, self.tiledata - 10)
        
        
class WaveTile(Tile):
    char = 'o'

    def update(self):
        frontbuffer = self.tiledata // 256
        backbuffer = self.tiledata % 256
        
        id = self.tileid
        
        tile_left_id = self.world._getTileID(self.x - 1, self.y)
        tile_right_id = self.world._getTileID(self.x + 1, self.y)
        tile_down_id = self.world._getTileID(self.x, self.y - 1)
        tile_up_id = self.world._getTileID(self.x, self.y + 1)
        
        if tile_left_id == id and tile_right_id == id:
            tile_left_data = self.world._getTileData(self.x - 1, self.y) % 256
            tile_right_data = self.world._getTileData(self.x + 1, self.y) // 256
        elif tile_left_id == id:
            tile_left_data = tile_right_data = self.world._getTileData(self.x - 1, self.y) % 256
        elif tile_right_id == id:
            tile_left_data = tile_right_data = self.world._getTileData(self.x + 1, self.y) // 256
        else:
            tile_left_data = tile_right_data = 0
            
        if tile_down_id == id and tile_up_id == id:
            tile_down_data = self.world._getTileData(self.x, self.y - 1) % 256
            tile_up_data = self.world._getTileData(self.x, self.y + 1) // 256
        elif tile_down_id == id:
            tile_down_data = tile_up_data = self.world._getTileData(self.x, self.y - 1) % 256
        elif tile_up_id == id:
            tile_down_data = tile_up_data = self.world._getTileData(self.x, self.y + 1) // 256
        else:
            tile_down_data = tile_up_data = 0
                
        backbuffer = int((tile_left_data+tile_right_data+tile_down_data+tile_up_data)/2)-backbuffer
        backbuffer = backbuffer - backbuffer // 16
        backbuffer = max(0, min(backbuffer, 255))

        self.tiledata = int(backbuffer) * 256 + frontbuffer
        
    
    def onEntry(self, entity):
        self.tiledata = 255*256
        return True
        
    def render(self):
        return self.char, self.tiledata >> 8
        
        