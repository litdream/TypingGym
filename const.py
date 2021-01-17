import pygame

TITLE = 'Welcome to the Typing Gym.'
BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
RED  =  ( 255,0,0)
DARK_RED = (127, 0, 0)
GREEN = ( 0, 255,0)
BLUE  = ( 0, 0, 255)
ORANGE = (255,165,0)
YELLOW = (255,255,0)

def load_location_file(fn="location.dat"):
    # Rough spacing:
    #   x 145-107 = 38
    rtn = dict()
    with open(fn) as fh:
        for l in fh:
            if len(l.strip()) == 0:
                continue
            arr = l.split()
            rtn[arr[0].strip()] = ( int(arr[1]), int(arr[2]))
    return rtn 

last_loaded = None
def load_and_play(fn):
    global last_loaded
    if last_loaded != fn:
        pygame.mixer.music.load(fn)
        last_loaded = fn
    pygame.mixer.music.play()
