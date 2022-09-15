import random
import st7789
import utime
from pimoroni import Button
from pimoroni import RGBLED

WIDTH, HEIGHT = 320, 240  # Pico Display 2.0
WAIT_UNTIL_NEXT_MOVE = 0.05 # the duration in seconds waited until the next move is performed
GRID_CONSTANT = 20 # integrally divisible (WIDTH / GRID_CONSTANT and HEIGHT / GRID_CONSTANT) to create a grid
MAX_KEYS = 7


display = st7789.ST7789(WIDTH, HEIGHT, rotate180=False)
display.set_backlight(0.5)

led = RGBLED(6, 7, 8)
led.set_rgb(0, 0, 0)

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

# generates a random position located on the grid
def rand_pos():
    x = random.randrange(0, WIDTH, GRID_CONSTANT)
    y = random.randrange(0, HEIGHT, GRID_CONSTANT)
    return (x, y)

def unique_pos(unique_for) -> (int, int):
    pos = rand_pos()
    while pos in unique_for:
        pos = rand_pos()
    return pos
    
def gen_rand_keys(min_keys: int, max_keys: int):
    key_count = random.randrange(min_keys, max_keys)
    keys = []
    
    for key_idx in range(key_count):
        keys.append(unique_pos(keys))
        
    return keys
    

def game_loop():
    keys = gen_rand_keys(2, MAX_KEYS)
    
    exit_door = unique_pos(keys)
    (px, py) = unique_pos(keys)
    
    keys_to_collect = len(keys)

    while True:
    
        # paint old player position black
        display.set_pen(0, 0, 0)
        display.rectangle(px, py, GRID_CONSTANT, GRID_CONSTANT)
    
        if button_a.read():
            px -= GRID_CONSTANT
        # move right
        if button_x.read():
            px += GRID_CONSTANT
            
        if button_b.read():
            py -= GRID_CONSTANT
            
        if button_y.read():
            py += GRID_CONSTANT
        
        if (px, py) in keys:
            keys_to_collect -= 1
            keys.remove((px, py))
    
        # draw keys
        display.set_pen(255, 220, 10)
    
        for (x, y) in keys:
            display.rectangle(x, y, GRID_CONSTANT, GRID_CONSTANT)        
    
        # draw exit
        display.set_pen(170, 120, 60)
        display.rectangle(exit_door[0], exit_door[1], GRID_CONSTANT, GRID_CONSTANT)    
    
        # draw player
        display.set_pen(90, 90, 90)
        display.rectangle(px, py, GRID_CONSTANT, GRID_CONSTANT)
    
        if keys_to_collect == 0 and (px, py) == exit_door:
            print("End")
    
        display.update()
        
        utime.sleep(WAIT_UNTIL_NEXT_MOVE)
        

if __name__ == "__main__":
    game_loop()
