import tcod as libtcod
from core.core import World, Entity
from core.tiles import GroundTile, WaveTile, SkyTile

import time
import numpy as np
#import cProfile

import warnings
warnings.simplefilter("ignore")

def main():
    screen_width = 80
    screen_height = 50
    
    colors = [ libtcod.Color(val, val, val) for val in range(256) ]

                
    #### Set up libtcod window
    libtcod.console_set_custom_font('arial10x10.png', 
        libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)
    root = libtcod.console_init_root(screen_width, screen_height, 
            'title', False, libtcod.RENDERER_SDL2, vsync=True)
    con = libtcod.console.Console(screen_width, screen_height)
    
    key = libtcod.Key()
    mouse = libtcod.Mouse()
    
    
    ### World creation
    tileset = {
            1: WaveTile,
            2: GroundTile,
            3: SkyTile,
          }
    
    # World generator function
    def pondgenerator(x, y):
        x_ = x - 40
        y_ = y - 20
        
        theta = np.arctan2(y_, x_)
        r = 15 + 4*np.cos(theta) - 8* np.sin(theta) + 6* np.cos(2*theta) - 6* np.sin(3*theta)
        r_ = r + np.random.randint(10)
        if x_*x_ + y_*y_ < r_*r_:
            return 1, 0
        if x_*x_ + y_*y_ > r_*r_ + 1500:
            return 3, 0   
        else:
            return 2, r_*4
    
    world = World(tileset=tileset, generator=pondgenerator, size=(screen_width, screen_height))
    
    
    #### Create player and add to the world
    player = world.createEntity(Entity, int(screen_width / 2), int(screen_height / 2), '@')
    world.avatar = player
    
    
    ### Game loop
    last_time_check = time.time()
    num_frames = 0
    frames_per_second = 0
    #pr = cProfile.Profile()
    while not libtcod.console_is_window_closed():
    
        #FPS counter
        num_frames = num_frames + 1
        if time.time() > last_time_check + 1:
            last_time_check = time.time()
            frames_per_second = num_frames
            num_frames = 0
        #pr.enable()
            
        # Update
        
        # Update input
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS, key, mouse)

        if key.vk == libtcod.KEY_ESCAPE:
            return True
            
        actiondict = {}
        if key.vk == libtcod.KEY_UP:
            actiondict["move"] = (0,-1)
        elif key.vk == libtcod.KEY_DOWN:
            actiondict["move"] = (0,1)
        elif key.vk == libtcod.KEY_LEFT:
            actiondict["move"] = (-1,0)
        elif key.vk == libtcod.KEY_RIGHT:
            actiondict["move"] = (1,0)
        
        # Update world
        world.update(actiondict=actiondict)
        
            
        # Render
        
        #Draw Tiles
        for x in range(world.width):
          for y in range(world.height):
            tile = world.getTile(x,y)
            
            char, val = tile.render()
            val = val if val is not 0 else 0
            con.draw_rect(x, y, 1, 1, ord(char), fg=libtcod.white, bg=colors[val])

        
        #Draw Entities
        for entity in world.entities:
            con.draw_rect(entity.x, entity.y, 1, 1, ord(entity.char), fg=libtcod.white)

            
        #Draw FPS counter
        time_str = "{:>3d}".format(frames_per_second)
        for i in range(3):
            libtcod.console_put_char(con, i, 0, time_str[i], libtcod.BKGND_NONE)
        
        
        # 'Flip' screen buffers
        con.blit(root)
        con.clear()
        libtcod.console_flush()
        
        #pr.disable()
        #if num_frames % 10 == 0:
        #    pr.print_stats()
            
            
if __name__ == '__main__':
    main()