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
    
    while not done:
        screen.fill(BLACK)

        text = font.render('abcdefg', True, BLUE)
        screen.blit(text, (100, 100))

        allSprites.update()
        allSprites.draw(screen)

        #
        # Event handle
        #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()

                
        # Scrolling
        typed_line = cur_line
        cur_line = next_line
        next_line = ' '.join(load_line(arr))

        clock.tick(60)
        pygame.display.flip()    
        done = ( len(cur_line.strip()) == 0 )
        print cur_line
        
def main_loop():
    global score
    pygame.init()
    pygame.display.set_caption(TITLE)

    article="alice.txt"
    main_screen(article)
    pygame.quit()
    
if __name__ == '__main__':
    main_loop()
