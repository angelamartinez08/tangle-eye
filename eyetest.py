#!/usr/bin/env python3
import pandas as pd
import numpy as np
from psychopy import visual
from lncdtask.lncdtask import (
    LNCDTask,
    create_window,
    replace_img,
    wait_for_scanner,
    ExternalCom,
    RunDialog,
    FileLogger,
)


def adjust_coord(x, img):
    """adjust point to be -1 to 1
    >>> adjust_coord(0, 1000)
    -1.0
    >>> adjust_coord(1000, 1000)
    1.0
    >>> adjust_coord(500, 1000)
    0.0
    """

    half = img / 2
    return (x - half) / half


def random_pos_df(dur: float, n: int) -> pd.DataFrame:
    """
    Make a list of where to show the dot. And shuffle
    >>> df = random_pos_df(1,1)
    >>> np.max(df['onset'])
    15
    >>> np.min(df['x']) # doctest: +ELLIPSIS
    -0.7...
    >>> np.max(df['x']) # doctest: +ELLIPSIS
    0.8...
    """
    img_size = (1366, 768)
    # fmt: off
    #: ROIs clicked through on gimp and path exported as ``eye_path_roi``
    #: hard copied into this list
    LOCATIONS=[( 292.0,  62.0, 'cmnt-cnt-NW' ),
               ( 180.0, 621.0, 'cmnt-cnt-icn-SW' ),
               ( 221.0, 622.0, 'cmnt-cnt-SW' ),
               ( 381.0, 624.0, 'like-cnt-icn-SW' ),
               ( 427.0, 623.0, 'like-cnt-SW' ),
               ( 596.0, 621.0, 'view-cnt-icn-SW' ),
               ( 650.0, 623.0, 'view-cnt-SW' ),
               ( 534.0, 254.0, 'face-NE' ),
               ( 890.0, 164.0, 'face-NW' ),
               (1238.0,  64.0, 'cmnt-cnt-NW' ),
               ( 821.0, 625.0, 'cmnt-cnt-icn-SW' ),
               ( 861.0, 623.0, 'cmnt-cnt-SE'  ),
               (1025.0, 626.0, 'like-cnt-icn-SE' ),
               (1070.0, 624.0, 'like-cnt-SE'  ),
               (1233.0, 625.0, 'view-cnt-icn-SE' ),
               (1287.0, 623.0, 'view-cnt-SE')  ]
    # fmt: on
    # test location math
    # LOCATIONS = [(1366-5,768-5,'bottom-right'),
    #             (1366-5,0,'bottom-left'),
    #             (0,0,'top-left'),
    #             (0,768-5,'bottom-left')]

    df = pd.DataFrame(LOCATIONS, columns=["x", "y", "desc"])
    df.loc[:, "x"] = adjust_coord(df["x"], img_size[0])
    #: Y in original ROIs is flipped: top is "1" here
    df.loc[:, "y"] = -1 * adjust_coord(df["y"], img_size[1])
    df["event_name"] = "dot"
    df = df.sample(frac=n)
    df["onset"] = np.arange(df.shape[0]) * dur
    return df


class TangleEyeTest(LNCDTask):
    """
    Show a dot over example background to get a measure of how well eye tracking works.
    NB. expect different percision in and out of the scanner
    """

    def __init__(self, *karg, **kargs):
        """create
        >> win = create_window(False)
        >> tangle = TangleEyeTest(win=win, externals=[printer])
        >> tangle.dot(0, .75)
        """
        super().__init__(*karg, **kargs)

        # extra stims/objects, exending base LNCDTask class
        self.trialnum = 0

        # example image (streched)
        self.background = visual.ImageStim(self.win, image="ppt_example.png")
        # relative units are -1 to 1. but size can't be negative. so realtive image size is 0 to 2
        self.background.size = [2, 2]

        # events
        self.add_event_type("dot", self.dot, ["onset", "x", "y", "desc"])

    def dot(self, onset, x=0, y=0, desc="dot"):
        """position dot on horz axis to cue anti saccade
        x and y position is from -1 to 1 (left-right, bottom-top)
        """
        self.trialnum = self.trialnum + 1
        self.background.draw()

        # guide to draw
        self.crcl.pos = (x * self.win.size[0] / 2, y * self.win.size[1] / 2)
        self.crcl.size = (1, 1)
        self.crcl.draw()

        # will send trigger
        return self.flip_at(onset, self.trialnum, desc, x, y)


def run():
    printer = ExternalCom()
    eyetracker = None
    # gui displayed to task administer
    run_info = RunDialog(
        extra_dict={
            "fullscreen": True,
            "dur": 1,
            "reps": 3,
            "tracker": ["eyelink", "None"],
        },
        order=["subjid", "run_num", "timepoint", "fullscreen", "dur"],
    )

    if not run_info.dlg_ok():
        sys.exit()

    dur = float(run_info.info["dur"])
    reps = int(run_info.info["dur"])

    # create task
    win = create_window(run_info.info["fullscreen"])
    onset_df = random_pos_df(dur=dur, n=reps)
    eyecal = TangleEyeTest(win=win, externals=[printer], onset_df=onset_df)
    eyecal.gobal_quit_key()  # escape quits
    eyecal.DEBUG = False

    participant = run_info.mk_participant(["TangleEyeTest"])
    run_id = f"{participant.ses_id()}_task-EC_run-{run_info.run_num()}"

    # when using eyelink, will setup so end of task copies edf file to this computer
    # also sends messages using trigger information with flips
    if run_info.info["tracker"] == "eyelink":
        from lncdtask.externalcom import Eyelink

        eyetracker = Eyelink(win.size)
        eyecal.externals.append(eyetracker)
        eyetracker.new(run_id)

    logger = FileLogger()
    logger.new(participant.log_path(run_id))
    eyecal.externals.append(logger)

    eyecal.run(end_wait=1)
    eyecal.onset_df.to_csv(participant.run_path(f"run-{run_info.run_num()}_info"))
    eyecal.msg(f"Thanks for playing!")
    win.close()


if __name__ == "__main__":
    run()
