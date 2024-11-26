# Tangle Eye tracking test

![Launching script](./eyetest_launch.png)

## Setup
`make test` will install [`lncdtasks`](https://github.com/LabNeuroCogDevel/lncdtask/) with pip in a venv and exercise `./eyetest.py`.

Run like
```
make test            # once to setup and confirm working
. .venv/activate/bin # per session to use locally-installed python libraries
./eyetest.py         # to get the task dialog box
```

For more eye tracking specific interface see 
  * [`pylink_help.py`](https://github.com/LabNeuroCogDevel/lncdtask/blob/main/lncdtask/pylink_help.py) for lncdtask code
  * https://rad.pitt.edu/wiki/doku.php?id=eyetracking:eyelink:task_integration for more info for use at the scanner
  * https://www.sr-research.com/support/thread-13.html for free-regirstation required SDK download on the EyeLink forums
