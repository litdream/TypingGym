import sys
import pygame
from pygame import *
from const import *
from keyboard import *

class RealKeyboard(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("real-keyboard.jpg").convert()
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x=5
        self.rect.y=300


location = None
def key_indicate(screen, color, punch):
    global location
    if not location:
        location = load_location_file()

    try:
        punch = punch.lower()
        loc = location[punch]
        pygame.draw.circle(screen, color, loc, 15, 4)
    except KeyError:
        if punch == ' ':
            pygame.draw.circle(screen, color, (280,545), 15, 4)

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

def decorate_key(prkey, shifted):
    rtn = prkey
    if shifted:
        if prkey == '[':   rtn = '{'
        elif prkey == ']':   rtn = '}'
        elif prkey == '1':   rtn = '!'
        elif prkey == '2':   rtn = '@'
        elif prkey == '3':   rtn = '#'
        elif prkey == '4':   rtn = '$'
        elif prkey == '5':   rtn = '%'
        elif prkey == '6':   rtn = '^'
        elif prkey == '7':   rtn = '&'
        elif prkey == '8':   rtn = '*'
        elif prkey == '9':   rtn = '('
        elif prkey == '0':   rtn = ')'
        elif prkey == '-':   rtn = '_'
        elif prkey == '=':   rtn = '+'
        elif prkey == '\\':  rtn = '|'
        elif prkey == ';':   rtn = ':'
        elif prkey == "'":   rtn = '"'
        elif prkey == ',':   rtn = '<'
        elif prkey == '.':   rtn = '>'
        elif prkey == '/':   rtn = '?'
    return rtn

def get_key_pressed(event):
    if event.key == pygame.K_a:   pressed_key = 'a'
    elif event.key == pygame.K_b:   pressed_key = 'b'
    elif event.key == pygame.K_c:   pressed_key = 'c'
    elif event.key == pygame.K_d:   pressed_key = 'd'
    elif event.key == pygame.K_e:   pressed_key = 'e'
    elif event.key == pygame.K_f:   pressed_key = 'f'
    elif event.key == pygame.K_g:   pressed_key = 'g'
    elif event.key == pygame.K_h:   pressed_key = 'h'
    elif event.key == pygame.K_i:   pressed_key = 'i'
    elif event.key == pygame.K_j:   pressed_key = 'j'
    elif event.key == pygame.K_k:   pressed_key = 'k'
    elif event.key == pygame.K_l:   pressed_key = 'l'
    elif event.key == pygame.K_m:   pressed_key = 'm'
    elif event.key == pygame.K_n:   pressed_key = 'n'
    elif event.key == pygame.K_o:   pressed_key = 'o'
    elif event.key == pygame.K_p:   pressed_key = 'p'
    elif event.key == pygame.K_q:   pressed_key = 'q'
    elif event.key == pygame.K_r:   pressed_key = 'r'
    elif event.key == pygame.K_s:   pressed_key = 's'
    elif event.key == pygame.K_t:   pressed_key = 't'
    elif event.key == pygame.K_u:   pressed_key = 'u'
    elif event.key == pygame.K_v:   pressed_key = 'v'
    elif event.key == pygame.K_w:   pressed_key = 'w'
    elif event.key == pygame.K_x:   pressed_key = 'x'
    elif event.key == pygame.K_y:   pressed_key = 'y'
    elif event.key == pygame.K_z:   pressed_key = 'z'
    elif event.key == pygame.K_0:   pressed_key = '0'
    elif event.key == pygame.K_1:   pressed_key = '1'
    elif event.key == pygame.K_2:   pressed_key = '2'
    elif event.key == pygame.K_3:   pressed_key = '3'
    elif event.key == pygame.K_4:   pressed_key = '4'
    elif event.key == pygame.K_5:   pressed_key = '5'
    elif event.key == pygame.K_6:   pressed_key = '6'
    elif event.key == pygame.K_7:   pressed_key = '7'
    elif event.key == pygame.K_8:   pressed_key = '8'
    elif event.key == pygame.K_9:   pressed_key = '9'
    elif event.key == pygame.K_SEMICOLON:  pressed_key = ';'
    elif event.key == pygame.K_PERIOD:     pressed_key = '.'
    elif event.key == pygame.K_COMMA:      pressed_key = ','
    elif event.key == pygame.K_QUOTE:      pressed_key = "'"
    elif event.key == pygame.K_SLASH:      pressed_key = "/"
    elif event.key == pygame.K_BACKQUOTE:  pressed_key = '`'
    elif event.key == pygame.K_MINUS:      pressed_key = '-'
    elif event.key == pygame.K_PLUS:       pressed_key = '+'
    elif event.key == pygame.K_EQUALS:     pressed_key = '='
    elif event.key == pygame.K_SPACE:      pressed_key = ' '
    elif event.key == pygame.K_RETURN:     pressed_key = '\r'
    elif event.key == pygame.K_BACKSPACE:  pressed_key = '\b'
    elif event.key == pygame.K_LEFTBRACKET: pressed_key = '['
    elif event.key == pygame.K_RIGHTBRACKET: pressed_key = ']'
    elif event.key in (K_LSHIFT, K_RSHIFT):  pressed_key = 'SHIFT'
    elif event.key in (K_LCTRL, K_RCTRL):    pressed_key = 'CTRL'
    elif event.key in (K_LALT, K_RALT):      pressed_key = 'ALT'
    else:
        pressed_key = None

    return pressed_key
