#!/usr/bin/env python2

import os
import sys
import pygame
import random
import copy
import time
import time_attack
from const import *
from keyboard import *
from word_dict import *
from time_attack import *

font_size = 15
score = 0
high_score = 0
config_dir = os.path.join(os.environ['HOME'], '.ytt')

def set_font(f):
    if f:
        return f

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


def clap(dura=5):
    screen = pygame.display.get_surface()
    clock = pygame.time.Clock()
    
    expire = time.time() + dura
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

            
def time_attack_round(castle, words, rnd, freq=60, speed=30, dura=60):
    global score, high_score
    
    font = set_font(None)
    clock = pygame.time.Clock()
    screen = pygame.display.get_surface()
    back_ground = pygame.image.load("m2_back.jpg").convert()    

    allSprites = pygame.sprite.Group()
    wordRains  = pygame.sprite.Group()
    allSprites.add(castle)

    userword = list()
    expire = time.time() + dura
    done = False 

    cnt =0
    next_freq = freq
    while not done:
        cnt += 1
        # TODO:
        #   Randomness for WordRain
        if time.time() < expire and cnt % next_freq == 0:
            idx = random.randint(0, len(words)-1)

            if cnt % 13 == 0:
                w = SpecialWord(words[idx], random.randint(0,600))
            else:
                w = WordRain( words[idx], random.randint(0,600))

            if time_attack.gExtraSpeed != -1:
                if not pygame.sprite.spritecollide(w, wordRains, None):
                    allSprites.add(w)
                    wordRains.add(w)
            #
            # Random frequency
            #   note:  this will occur more often than just regular frequency.
            #          
            next_freq = freq + ( random.randint(0, freq) - (freq/2))
            
        screen.fill(BLACK)
        screen.blit(back_ground, (0,0))
        cur_score = font.render("score: %08d           high score: %08d          level: %d" % (score,high_score, rnd) , True, WHITE)
        screen.blit(cur_score, (5,5))
        
        pressed_key = None
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and ( event.mod & pygame.KMOD_LCTRL ):
                    pygame.quit()
                pressed_key = get_key_pressed(event)
                
        if pressed_key:
            if pressed_key == ' ' or pressed_key == '\r':
                for sp in wordRains:
                    if sp.word == ''.join(userword):
                        load_and_play("barrel-explode.ogg")
                        score += rnd * 10
                        time.sleep(0.2)
                        wordRains.remove(sp)
                        allSprites.remove(sp)

                        if hasattr(sp, 'special'):
                            wipe_score = 0
                            if sp.special == Special.wipe:
                                wipe_score = (rnd * 10) * len(wordRains)
                            sp.do_special(castle, wordRains, allSprites)
                            score += wipe_score
                            
                userword = list()
            elif pressed_key == '\b':
                if userword:
                    userword.pop()
            else:
                userword.append(pressed_key)

        if score > high_score:
            high_score = score
            
        # TODO:
        #   Detect Hit/Miss
        for sp in wordRains:
            if sp.rect.y > 550:
                wordRains.remove(sp)
                allSprites.remove(sp)
                
                if not castle.hit_and_check():
                    # Lost all health.
                    #   TODO:  Better lost message.
                    print("------------------------------------")
                    print("You Lost")
                    print("------------------------------------")

                    with open( os.path.join( config_dir, 'data')) as fh:
                        fh.write('highscore = %d' % high_score)

                    pygame.quit()


        # Render
        #   0. background
        allSprites.update()
        allSprites.draw(screen)

        # User input area:
        #   - 227,465 (width:146)
        pygame.draw.rect(screen, BLACK, (227,465,146,20))

        # Text print
        if len(userword) <=16:
            text = font.render(''.join(userword), True, WHITE)
        else:
            text = font.render(''.join(userword[-16:]), True, WHITE)
        screen.blit(text, (229, 467))

        clock.tick(speed)
        pygame.display.flip()

        if time.time() > expire and len(wordRains) == 0:
            done = True

            
def main_loop():
    global score
    
    pygame.init()
    font = set_font(None)
    pygame.display.set_caption(TITLE)
    screen = pygame.display.set_mode((600,600))

    from time_attack import Castle
    castle = Castle()
    
    done = False
    all_words = get_all_levels()

    words = None
    freq, speed, dura = 130, 30, 70
    for i in range(0, 11):
        if words is None:
            words = copy.deepcopy(all_words[i])
        else:
            words += all_words[i]
        time_attack_round(castle, words + all_words[i] + all_words[i], i+1, freq, speed, dura)   # more current level words!
        clap()
        speed *= 1.1
        dura  *= 1.06 

    for i in range(11, 99):
        time_attack_round(castle, words, i+1, freq, speed, dura)
        dura *= 1.16
        speed *= 1.1
        
    pygame.quit()
    
    
if __name__ == '__main__':
    if not os.path.exists( config_dir):
        os.mkdir(config_dir)
        os.system('touch %s' % os.path.join(config_dir, 'data'))
    global high_score
    with open( os.path.join( config_dir, 'data')) as fh:
        for l in fh:
            if l.startswith('highscore ='):
                l = l.strip().replace('highscore = ', '')
                high_score = int(l)
    main_loop()
