#!/usr/bin/env python
from __future__ import print_function

scriptId          = "classify_svm"
scriptTitle       = "SVM Classifier"
scriptDescription = "Uses the SKLearn SVM implemantation to Classify up to 10 Gestures"


import sys, time
import struct
from collections import Counter

#import myo
import numpy as np
from sklearn import neighbors, svm

import pygame
from pygame.locals import *

w, h = 800, 320
scr = None
font = None

def onOn():
  pygame.init()
  global scr 
  scr = pygame.display.set_mode((w, h))
  global font
  font = pygame.font.Font(None, 30)
  pass

def onOff():
  pygame.display.quit()
  pygame.quit()
  pass

recording = -1
emg_last  = (0,) * 8
def onEMG(emg, moving):
  global recording
  global emg_last
  
  emg_last = emg
  if recording >= 0:
    myo.cls.store_data(recording, emg)
    pass
  
  dataset = list(myo.getAccel()) + [g / 360. for g in myo.getGyro()] + [e / 2000. for e in emg]
  plot(scr, dataset)
  pass

def onPeriodic():
  # handle events
  global recording
  for ev in pygame.event.get():
    if ev.type == KEYDOWN:
      if K_0 <= ev.key <= K_9:
        recording = ev.key - K_0
      elif K_KP0 <= ev.key <= K_KP9:
        recording = ev.key - K_Kp0
    elif ev.type == KEYUP:
      if K_0 <= ev.key <= K_9 or K_KP0 <= ev.key <= K_KP9:
        recording = -1
        
  # show displays
  global w, h
  scr.fill((0, 0, 0), (0, 0, w, h))
  r = myo.history_cnt.most_common(1)[0][0]
  for i in range(10):
    x = 0
    y = 0 + 30 * i

    clr = (0,200,0) if i == r else (255,255,255)

    txt = font.render('%5d' % (myo.cls.Y == i).sum(), True, (255,255,255))
    scr.blit(txt, (x + 20, y))

    txt = font.render('%d' % i, True, clr)
    scr.blit(txt, (x + 110, y))


    scr.fill((0,0,0), (x+130, y + txt.get_height() / 2 - 10, len(myo.history) * 20, 20))
    scr.fill(clr, (x+130, y + txt.get_height() / 2 - 10, myo.history_cnt[i] * 20, 20))
  pygame.display.flip()
  pass


