#!/usr/bin/env python3
"""
move some text across the screen to simulate scrolling
"""

from psychopy import visual, core
import logging
import numpy as np

logging.basicConfig(level=logging.INFO)


win = visual.Window([800, 600])
start = win.flip()
text = visual.TextStim(win=win, text='Hello')
shape = visual.Circle(win=win, radius=.2, color='yellow', pos=(0,-.6))
step_size=.01

text.pos=(0,.5)
final_pos = 1
max_dur = 3

print(f"starting with y pos = {text.pos[1]} (to {final_pos}) at time {start}")
onset = 0
while final_pos > text.pos[1] and (onset - start) < max_dur:
    text.pos = (text.pos[0], text.pos[1] + step_size)
    # shape.pos[1] += step_size # -- doesn't work. need to set whole pos tuple
    shape.pos = (shape.pos[0], shape.pos[1] + step_size)
    text.text=f"moved to {text.pos[1]:.2f}; {onset-start:.2f}s in"
    shape.draw()
    text.draw()
    #core.wait(.033)
    onset = win.flip()
print(f"finished w/y pos={text.pos[1]} at {onset}s")



core.wait(.5)
core.quit()


