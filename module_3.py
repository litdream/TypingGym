#!/usr/bin/env python2

import sys
import pygame
import random
import copy
import time
from const import *
from keyboard import *

# Alice in Wonderland were from gutenberg.org.
#   https://www.gutenberg.org/ebooks/28885

class WordLine(pygame.sprite.Sprite):
    def __init__(self, font, color, line):
        pygame.sprite.Sprite.__init__(self)
        self.line = line
        self.font = font
        self.image = self.font.render( self.line, True, color)
        self.rect = self.image.get_rect()
        self.rect.x = 10
        self.rect.y = 280
        self.target_y = 250
        
    def update(self):
        while self.rect.y > self.target_y:
            self.rect.y -= 5

    def move_up(self):
        self.target_y -= 100

        
class UserLine(pygame.sprite.Sprite):
    def __init__(self, font):
        self.font = font

    def match_render(self, userlist, linelist):
        pass
        
font_size=20
def set_font():
    font = None
    if 'freemono' in pygame.font.get_fonts():
        # Linux
        font = pygame.font.SysFont("freemono", font_size)
    elif 'menlo' in pygame.font.get_fonts():
        # Apple
        font = pygame.font.SysFont("menlo", font_size)
    else:
        # Windows
        font = pygame.font.SysFont("consolas", font_size)
    return font

def load_line(lst, line_length=50):
    rtn = list()
    while lst and line_length > len(' '.join(rtn)):
        rtn.append(lst.pop())
    if line_length > len(' '.join(rtn)):
        lst.append(rtn.pop())
    return rtn

def main_screen(fname):
    arr = list()
    with open(fname) as fh:
        for l in fh:
            if len(l.strip()) == 0: continue
            arr += l.strip().split()
    arr.reverse()

    screen = pygame.display.set_mode((600,600))
    allSprites = pygame.sprite.Group()
    keyimg = RealKeyboard()
    allSprites.add(keyimg)

    done = False
    pressed_key = None
    clock = pygame.time.Clock()
    user = list()

    font =set_font()
    i = 0
    leave_key = None

    typed_line = None
    cur_line = ' '.join(load_line(arr))
    next_line = ' '.join(load_line(arr))

    user_line = list()

    # TEST
    l = WordLine(font,  WHITE, cur_line)
    l.move_up()
    allSprites.add(l)
    
    l2 = WordLine(font, WHITE, next_line)
    allSprites.add(l2)

    while not done:
        screen.fill(BLACK)
        #
        # Event handle
        #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()


        allSprites.update()
        allSprites.draw(screen)
                
                
        # Scrolling
        typed_line = cur_line
        cur_line = next_line
        next_line = ' '.join(load_line(arr))

        clock.tick(90)
        pygame.display.flip()    
        #done = ( len(cur_line.strip()) == 0 )

        
def main_loop():
    global score
    pygame.init()
    pygame.display.set_caption(TITLE)

    article="alice.txt"
    main_screen(article)
    pygame.quit()
    
if __name__ == '__main__':
    main_loop()
