#!/usr/bin/env python2

import os
import sys
import random

def main():
    all_words = dict()
    for i in range(0, 11):
        all_words[i] = list()

    fn = "flocabulary"
    try:
        if os.path.exists(sys.argv[1].strip()):
            fn = sys.argv[1].strip()
    except:
        pass
        
    with open(fn) as fh:
        for word in fh:
            if len(word.strip()) <3:
                continue
            if word.startswith("http"):
                continue
            
            word = word.strip().lower()
            s = set(word.strip())
            if s - set("asdf") == set():
                all_words[0].append(word)
            elif s - set("asdfjkl") == set():
                all_words[1].append(word)
            elif s - set("asdfjklqwer") == set():                
                all_words[2].append(word)
            elif s - set("asdfjkluiop") == set():
                all_words[3].append(word)
            elif s - set("asdfjklqweruiop") == set():
                all_words[4].append(word)
            elif s - set("asdfjklzxcvm") == set():
                all_words[5].append(word)
            elif s - set("asdfjkltgb") == set():
                all_words[6].append(word)
            elif s - set("asdfjklyhn") == set():
                all_words[7].append(word)
            elif s - set("asdfjkltgbyhn") == set():
                all_words[8].append(word)
            elif s - set("asdfjklqweruiopzxcvnm") == set():
                all_words[9].append(word)
            elif s - set("abcdefghijklmnopqrstuvwxyz") == set():
                all_words[10].append(word)
            else:
                pass

    for i in range(0,11):
        print("Level %d" % i)
        lst = all_words[i]
        random.shuffle(lst)

        if len(lst) > 50:
            for w in lst[0:50]:
                print("   %s" % w)
        else:
            for w in lst:
                print("   %s" % w)
                
            
if __name__ == '__main__':
    main()

