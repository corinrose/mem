```
usage: mem.py [-h] [-t | -p | -l]

Analyze system memory usage via smem.

options:
  -h, --help  show this help message and exit
  -t, --tui   Display Rich TUI memory breakdown
  -p, --pie   Generate graphical pie chart using matplotlib
  -l, --list  Print text list breakdown
```

A simple memory usage analyzer, utilizing `smem` and pandas. This is mostly a fun project for me to get back into coding, but it does fill a niche that I have been unable to find: unlike other terminal system monitors like `htop`, this utility dynamically groups all processes associated with an application, so you can get a clearer picture of how much memory a multi threaded application (like a web browser) is using in total. This is a work in progress, and is not guaranteed to catch all processes, or could miss some.
