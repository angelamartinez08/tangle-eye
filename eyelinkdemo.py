#!/usr/bin/env python3
"""
quick demo with psychopy and eyelink
https://www.youtube.com/watch?v=1tLJHVktrEk
"""
import pandas as pd
import numpy as np
from psychopy import visual
import lncdtask.pylink_help as eye
import time


def main():

    win = visual.Window([800, 600])

    # a background image to show
    background = visual.ImageStim(win, image="ppt_example.png")
    # relative units are -1 to 1. but size can't be negative. so realtive image size is 0 to 2
    background.size = [2, 2]


    ### a circle we can move around
    dot = visual.Circle(win, radius=.1, lineColor=None, fillColor='yellow')
    dot.pos = (0,0)

    ## fixation cross
    fix = visual.TextStim(win, text='+',color='white', bold=True)


    ## eye tracking camera setup -- set eyelink ip to '' for dummy mode
    #  dummy mode still requires installing dev kit
    camera = eye.eyelink(win.size) #, ip='')

    ## implemeted as camera.open()
    # here for demo
    #
    # edf on eyetracker limited to 8 characters
    # hacky way to unix epoch seconds time to 8char
    time_encoded_name = eye.seconds_36base()
    print(time_encoded_name)
    camera.el.openDataFile(time_encoded_name + '.EDF')
    camera.el.sendMessage(f"NAME: {time_encoded_name}")

    # camera.start()
    camera.el.sendMessage("START")

    ### "Task"
    win.flip()
    fix.draw()
    win.flip()

    # see camera.trial_start(1)
    camera.el.sendMessage(f"TRIALID 1")
    fix.draw() 
    win.flip()
    # below same as camera.trigger(eventname)
    eventname = 'fix'
    camera.el.sendMessage(eventname)
    camera.el.sendCommand(f"record_status_message {eventname}")
    # next event
    eventname = 'dot'
    dot.draw()
    win.callOnFlip(camera.trigger, eventname)
    time.sleep(1)  # sleep after everything is setup up
    win.flip()
    camera.el.sendMessage("TRIAL OK")

    ####
    ## trial 2
    ####
    camera.trial_start(2)
    fix.draw()
    win.callOnFlip(camera.trigger, 'fix')
    time.sleep(1)
    win.flip()

    dot.pos=(.5, -.9)
    dot.draw()
    win.callOnFlip(camera.trigger, 'dot')
    time.sleep(1)
    win.flip()
    camera.trial_end() # could be part of flip hook



    time.sleep(1)
    # also see camera.stop()
    camera.el.sendMessage("END")
    camera.el.closeDataFile()
    save_as = f"localname-{time_encoded_name}.edf"
    camera.el.receiveDataFile("",save_as)
    win.close()


if __name__ == "__main__":
    main()
