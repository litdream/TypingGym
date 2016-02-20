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

font_size=15
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

def main_screen(fname):
    arr = list()
    with open(fname) as fh:
        for l in fh:
            if len(l.strip()) == 0: continue
            arr.append(l.strip())
    txt = ' '.join(arr)

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


        clock.tick(60)
        pygame.display.flip()    
        
    
def main_loop():
    global score
    pygame.init()
    pygame.display.set_caption(TITLE)

    article="alice.txt"
    main_screen(article)
    pygame.quit()
    
if __name__ == '__main__':
    main_loop()
