#!/usr/bin/env python2

import sys
import pygame
import random
import copy
import time
from const import *
from keyboard import *
from word_dict import *

font_size = 40
score = 0
inc=0

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


def clap():
    screen = pygame.display.set_mode((600,600))
    clock = pygame.time.Clock()
    
    expire = time.time() + 1.5
    img1 = pygame.image.load("clap1.png").convert()
    img2 = pygame.image.load("clap2.png").convert()

    img = img1
    load_and_play('applause.ogg')
    while time.time() < expire:
        screen.fill(BLACK)
        screen.blit(img, (100,100))

        clock.tick(10)
        pygame.display.flip()    

        if img == img1:
            img = img2
        else:
            img = img1
    
def question_loop(word):
    global score
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
        
        text = font.render("score: %06d" % score, True, WHITE)
        screen.blit(text, (250, 10))
        text = font.render(word, True, BLUE)
        screen.blit(text, (100, 100))

        # Render
        #   0: Background keyboard
        #      and Expected indicators.
        allSprites.update()
        allSprites.draw(screen)
        key_indicate(screen, ORANGE, word[i])
        finger_indicate(screen, BLUE, word[i])
        if leave_key:
            key_indicate(screen, RED, leave_key)
            
        #
        # Event handle
        #
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                
            elif event.type == pygame.KEYDOWN:
                # TODO:
                #   Move back up, rather than quit.
                if event.key == pygame.K_q and ( event.mod & pygame.KMOD_LCTRL ):
                    pygame.quit()
                pressed_key = get_key_pressed(event)

                # Early Sound Feedback
                if pressed_key == word[i]:
                    load_and_play('key_press.ogg')
                    i += 1
                    user.append(pressed_key)
                    leave_key = None
                else:
                    load_and_play('pig-oink.ogg')
                    leave_key = pressed_key
                    score -= 1
                    
        # Render
        #   1: User feedback
        if pressed_key:
            text = font.render(''.join(user), True, GREEN)
            screen.blit(text, (100, 150))

        clock.tick(60)
        pygame.display.flip()    
        done = word == ''.join(user)
    score += inc * len(word.strip())
    
def key_practice(strlist, repeat=3):
    global score
    global inc
    
    q = list(copy.deepcopy(strlist) * repeat)
    random.shuffle(q)
    while q:
        question_loop(q.pop())

def word_practice(wordlist, cnt=20):
    global score
    global inc
    
    q = copy.deepcopy(wordlist)
    random.shuffle(q)
    while cnt > 0:
        if not q:
            q = copy.deepcopy(wordlist)
            random.shuffle(q)
        question_loop(q.pop())
        cnt -=1
    
def main_loop():
    global score
    pygame.init()
    pygame.display.set_caption(TITLE)
    
    cnt = 0
    all_words = get_all_levels()

    # Program Path
    def _lvl_player(keys, words, kcnt=3, wcnt=15, increment=1):
        global inc
        inc = increment
        
        key_practice(keys, kcnt)
        clap()
        word_practice(words, wcnt)
        clap()
    
    _lvl_player("asdf", all_words[0], 5, 10, increment=1)
    _lvl_player("jkl;", all_words[0] + all_words[1], 3, 30, increment=2)
    _lvl_player("qwer", all_words[2], 5, 20, increment=3)
    _lvl_player("uiop", all_words[3], 5, 20, increment=4)
    _lvl_player("qweruiop", all_words[4], 3, 15, increment=5)
    _lvl_player("zxcvm", all_words[5], increment=6)
    _lvl_player("tgb", all_words[6], increment=7)
    _lvl_player("yhn", all_words[7], increment=8)
    _lvl_player("tgbyhn", all_words[8], increment=9)
    _lvl_player("asdfjklqweruiopzxcvnm", all_words[9], 1, increment=10)
    _lvl_player("asdfjkltgbyhn", all_words[10], 2, increment=11)

    pygame.quit()
    
if __name__ == '__main__':
    main_loop()
