import random
import pygame
import time
from const import *
from threading import Timer

class Castle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("castle_12.jpg").convert()
        self.rect = self.image.get_rect()
        self.life = 12

    def hit_and_check(self):
        self.life -= 1
        load_and_play("pig-oink.ogg")
        if self.life >0:
            self.image = pygame.image.load("castle_%d.jpg" % self.life).convert()
            self.rect = self.image.get_rect()
        return self.life >0
    
    def restore(self):
        self.life = 12
        self.image = pygame.image.load("castle_12.jpg").convert()
        
    def update(self):
        self.rect.x=227
        self.rect.y=465

        
def set_font(font_size):
    font = None
    if 'freemono' in pygame.font.get_fonts():
        # Linux
        font = pygame.font.SysFont("freemono", font_size)
    elif 'menlo' in pygame.font.get_fonts():
        # Apple
        font = pygame.font. SysFont("menlo", font_size)
    else:
        # Windows
        font = pygame.font.SysFont("consolas", font_size)
    return font

gExtraSpeed = 0
gSlowDown = 0
gHide = 0
class WordRain(pygame.sprite.Sprite):
    def __init__(self, word, x):
        pygame.sprite.Sprite.__init__(self)

        global font
        self.word = word
        self.color = DARK_RED
        self.setup_word()
        self.rect.x = x
        self.rect.y = 18
        self.clk = 0
        
        # If somehow word were too long for screen,
        sz = self.image.get_size()
        if x + sz[0] > 590:
            self.rect.x = 590 - sz[0]

    def setup_word(self):
        self.font = set_font(20)
        self.image1 = self.font.render(self.word, True, self.color)
        self.image2 = self.font.render('_' * len(self.word), True, self.color)
        self.image = self.image1
        self.rect  = self.image.get_rect()
        
    def update(self):
        global gExtraSpeed, gSlowDown
        self.clk += 1
        
        if gSlowDown and self.clk % 2==0:
            return
        if gHide:
            self.image = self.image2
        else:
            self.image = self.image1
            
        self.rect.y += 1 + gExtraSpeed


# Intentionally not using `Enum` for backward compatibility
# Later, use `Enum` with duck typing for old/new compatible.
#
class Special:
    hide, fast, slow, stop, recover, wipe = range(6)
    rev_lookup = [ hide, fast, slow, stop, recover, wipe ]


class SpecialWord(WordRain):
    def __init__(self, word, x):
        WordRain.__init__(self, word, x)
        self.color = YELLOW        
        self.setup_word()
        self.special = random.randint(0, len(Special.rev_lookup))

    def do_special(self, castle, wg, allg):
        if self.special == 0:
            global gHide
            gHide = 1
            def _reset_hide():
                global gHide
                gHide = 0
            Timer(5, _reset_hide, ()).start()
        
        elif self.special == 1:
            global gExtraSpeed
            gExtraSpeed = 1
            def _reset_speed():
                global gExtraSpeed
                gExtraSpeed = 0
            Timer(5, _reset_speed, ()).start()

        elif self.special == 2:
            global gSlowDown
            gSlowDown = 1
            def _reset_speed():
                global gSlowDown
                gSlowDown = 0
            Timer(5, _reset_speed, ()).start()

        elif self.special == 3:
            global gExtraSpeed
            gExtraSpeed = -1
            def _reset_speed():
                global gExtraSpeed
                gExtraSpeed = 0
            Timer(5, _reset_speed, ()).start()
            
        elif self.special == 4:
            castle.restore()

        elif self.special == 5:
            for sp in wg:
                load_and_play("barrel-explode.ogg")
                time.sleep(0.2)
                wg.remove(sp)
                allg.remove(sp)
            
