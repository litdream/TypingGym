#!/usr/bin/env python2

import sys
import pygame
import random
import time

BLACK = ( 0, 0, 0)
WHITE = ( 255, 255, 255)
RED  =  ( 255,0,0)
GREEN = ( 0, 255,0)
BLUE  = ( 0, 0, 255)

location = dict()

class RealKeyboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("real-keyboard.jpg").convert()
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x=5
        self.rect.y=300

def key_indicate(screen, color, punch):
    loc = location[punch]
    pygame.draw.circle(screen, color, loc, 15, 4)


def finger_indicate(screen, color, punch):
    def _triangle(offset, fill=False):
        lst = [ (105+offset, 310),
                (85+offset, 340),
                (125+offset, 340)  ]
        if fill:
            pygame.draw.polygon(screen, color, lst , 0)        
        else:
            pygame.draw.polygon(screen, color, lst , 4)        

    for i in range(0, 160, 40):
        if i==0 and punch in "qaz`1":
            _triangle(i, True)
        elif i==40 and punch in "wsx2":
            _triangle(i, True)
        elif i==80 and punch in "edc3":
            _triangle(i, True)
        elif i==120 and punch in "rfvtgb45":
            _triangle(i, True)
        else:
            _triangle(i)
            
    for i in range(180, 340, 40):
        if i==180 and punch in "yhnujm67":
            _triangle(i, True)
        elif i==220 and punch in "ik,8":
            _triangle(i, True)
        elif i==260 and punch in "ol.9":
            _triangle(i, True)
        elif i==300 and punch in "p;/[']\\0-+=":
            _triangle(i, True)
        else:
            _triangle(i)

last_loaded = None
def load_and_play(fn):
    global last_loaded
    if last_loaded != fn:
        pygame.mixer.music.load(fn)
        last_loaded = fn
    pygame.mixer.music.play()

    
def load_location_file():
    # Rough spacing:
    #   x 145-107 = 38
    rtn = dict()
    with open("location.dat") as fh:
        for l in fh:
            if len(l.strip()) == 0:
                continue
            arr = l.split()
            rtn[arr[0].strip()] = ( int(arr[1]), int(arr[2]))
    return rtn

if __name__ == '__main__':
    pygame.init()

    screen = pygame.display.set_mode((600,600))
    clock = pygame.time.Clock()

    allSprites = pygame.sprite.Group()
    keyimg = RealKeyboard()
    allSprites.add(keyimg)
    
    
    done = False
    pressed_key = None

    cnt = 0
    while not done:
        cnt +=1
        screen.fill(BLACK)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and ( event.mod & pygame.KMOD_LCTRL ):
                    pygame.quit()

                location = load_location_file()
                load_and_play('key_press.ogg')
                if cnt % 20 == 0:
                    load_and_play('pig-oink.ogg')
                if event.key == pygame.K_a:   pressed_key = 'a'
                if event.key == pygame.K_b:   pressed_key = 'b'
                if event.key == pygame.K_c:   pressed_key = 'c'
                if event.key == pygame.K_d:   pressed_key = 'd'
                if event.key == pygame.K_e:   pressed_key = 'e'
                if event.key == pygame.K_f:   pressed_key = 'f'
                if event.key == pygame.K_g:   pressed_key = 'g'
                if event.key == pygame.K_h:   pressed_key = 'h'
                if event.key == pygame.K_i:   pressed_key = 'i'
                if event.key == pygame.K_j:   pressed_key = 'j'
                if event.key == pygame.K_k:   pressed_key = 'k'
                if event.key == pygame.K_l:   pressed_key = 'l'
                if event.key == pygame.K_m:   pressed_key = 'm'
                if event.key == pygame.K_n:   pressed_key = 'n'
                if event.key == pygame.K_o:   pressed_key = 'o'
                if event.key == pygame.K_p:   pressed_key = 'p'
                if event.key == pygame.K_q:   pressed_key = 'q'
                if event.key == pygame.K_r:   pressed_key = 'r'
                if event.key == pygame.K_s:   pressed_key = 's'                    
                if event.key == pygame.K_t:   pressed_key = 't'
                if event.key == pygame.K_u:   pressed_key = 'u'
                if event.key == pygame.K_v:   pressed_key = 'v'
                if event.key == pygame.K_w:   pressed_key = 'w'
                if event.key == pygame.K_x:   pressed_key = 'x'
                if event.key == pygame.K_y:   pressed_key = 'y'
                if event.key == pygame.K_z:   pressed_key = 'z'
                if event.key == pygame.K_0:   pressed_key = '0'
                if event.key == pygame.K_1:   pressed_key = '1'
                if event.key == pygame.K_2:   pressed_key = '2'
                if event.key == pygame.K_3:   pressed_key = '3'
                if event.key == pygame.K_4:   pressed_key = '4'
                if event.key == pygame.K_5:   pressed_key = '5'
                if event.key == pygame.K_6:   pressed_key = '6'
                if event.key == pygame.K_7:   pressed_key = '7'
                if event.key == pygame.K_8:   pressed_key = '8'
                if event.key == pygame.K_9:   pressed_key = '9'
                if event.key == pygame.K_SEMICOLON:  pressed_key = ';'
                if event.key == pygame.K_PERIOD:     pressed_key = '.'
                if event.key == pygame.K_COMMA:      pressed_key = ','
                if event.key == pygame.K_QUOTE:      pressed_key = "'"
                if event.key == pygame.K_SLASH:      pressed_key = "/"
                if event.key == pygame.K_BACKQUOTE:  pressed_key = '`'
                if event.key == pygame.K_MINUS:      pressed_key = '-'
                if event.key == pygame.K_PLUS:       pressed_key = '+'
                if event.key == pygame.K_EQUALS:     pressed_key = '='
                    
        allSprites.update()
        allSprites.draw(screen)

        # Current key cursor
        if pressed_key:
            key_indicate(screen, RED, pressed_key)
            finger_indicate(screen, BLUE, pressed_key)

            if 'freemono' in pygame.font.get_fonts():
                # Linux
                font = pygame.font.SysFont("freemono", 40)
            elif 'monica' in pygame.font.get_fonts():
                # Apple
                font = pygame.font.SysFont("monica", 40)
            else:
                # Windows
                font = pygame.font.SysFont("consolas", 40)
                
            text = font.render(pressed_key, True, GREEN)
            screen.blit(text, (100, 100))
            
        clock.tick(60)
        pygame.display.flip()

    pygame.quit()
