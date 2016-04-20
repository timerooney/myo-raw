#!/usr/bin/env python
from __future__ import print_function

scriptId          = "plot_raw"
scriptTitle       = "Raw Data Plotter"
scriptDescription = "Plots acceleration, gyros and EMG values"

# needs pygame
import pygame
from pygame.locals import *

w, h = 1200, 400
scr = None

# helper function for plotting
# vals must be between 0. and 1.
last_vals = None
last_vals_width = 0        
def plot(scr, vals):
  DRAW_LINES = True

  global last_vals
  global last_vals_width
  if last_vals is None:
    last_vals = vals
    last_vals_width = len(vals)
    return

  D = 5
  scr.scroll(-D)
  scr.fill((0,0,0), (w - D, 0, w, h))
  for i, (u, v) in enumerate(zip(last_vals, vals)):
    if DRAW_LINES:
      pygame.draw.line(scr, (0,255,0),
                       (w - D, int(h/last_vals_width * (i+1 - u))),
                       (w, int(h/last_vals_width * (i+1 - v))))
      pygame.draw.line(scr, (255,255,255),
                       (w - D, int(h/last_vals_width * (i+1))),
                       (w, int(h/last_vals_width * (i+1))))
    else:
      c = int(255 * max(0, min(1, v)))
      scr.fill((c, c, c), (w - D, i * h / last_vals_width, D, (i + 1) * h / last_vals_width - i * h / last_vals_width));

  pygame.display.flip()
  last_vals = vals

def onOn():
  global scr 
  scr = pygame.display.set_mode((w, h))
  pass

def onOff():
  pygame.display.quit()
  pygame.quit()
  pass

def onEMG(emg, moving):
  dataset = list(myo.getAccel()) + [g / 360. for g in myo.getGyro()] + [e / 2000. for e in emg]
  plot(scr, dataset)
  pass