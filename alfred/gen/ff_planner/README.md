# Metric FF Planner
Credit: https://fai.cs.uni-saarland.de/hoffmann/metric-ff.html.  
Specifically this uses the Metric-FF Version 2.1 (https://fai.cs.uni-saarland.de/hoffmann/ff/Metric-FF-v2.1.tgz).

Note that the code here is not exactly the same as the one you can download from that website.
Their code had issues that threw segfaults which I was able to fix for this project.
It is possible that my changes caused some other issues that I am unaware of.

To compile:
```bash
$ cd
$ make
```


#Notes from Sam:
Had to make sure I was using gcc 7 (on mac: `brew install gcc@7`, then use gcc-7 in the Makefile). Other versions
may also work - I have reason to believe any of 6-9 are okay.
```
conda install -c conda-forge/label/gcc7 flex
```
