1)	The code must be run with python3
2)	Before running the code, you must have all the images in a folder called “yalefaces” in the current working directory. 
The scripts must be in the current working directory as well. The scripts make dynamic adjustments to the file path based on 
the OS you are running it from, so no further action is need before running.
3)	While running the code on tux, if you get the error “illegal instruction (core dumped)”, this suggests there is something 
wrong with the installation of some packages. To remedy this, I had to type “pip3 install --user numpy”. You might have to run 
the same command on your tux terminal.
4)	Alternatively, you can also run the code on your local machine. My scripts use common libraries so you should have no 
difficulty running it on tux. Libraries needed are, pillow, numpy, matplotlib, platform and glob.
5)	If you are still having trouble running the code I can send you my conda environment or a virtual environment. That will 
ensure we are running the scripts under the same dependencies. 
