`usage: mem.py [-h] [-t | -p | -l]

Analyze system memory usage via smem.

options:
  -h, --help  show this help message and exit
  -t, --tui   Display Rich TUI memory breakdown
  -p, --pie   Generate graphical pie chart using matplotlib
  -l, --list  Print text list breakdown`

A simple memory usage analyzer, utilizing `smem` and pandas. This functionality is largley if not entirely covered by `smem`--this is simply a project for me to play around after not coding recently.
