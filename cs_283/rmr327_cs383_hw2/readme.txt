'clustuting.py' was developed to be run in python 3.

The preferred player for playing the '.avi' video files is VLC Viewer.

To run the file, simply make sure your data file location is stated in the data_path variable inside
the innit method of the class 'Clustering'. The default data path location is set to look for
diabetes.csv in the current working directory.

Once you run the script 'clusturing.py', the program is going to as for k and the indices of the
features you want to use from your csv data file. For k you can just simple enter the desired k.
For feature indices, one thing to note is that the column index for the features start at 1. So,
the first feature starts at index 1. Example 1 : if you want the second and third features of a data set enter :2,3
Example 2: For diabetes.csv if you wanted to run for all features please enter:1,2,3,4,5,6,7,8

The modules needed to run this script are as follows:
pandas
numpy
copy
matplotlib
mpl_toolkits
cv2

If you are running on tux, if any modules are missing simple install it to you local user by
typing in the following:
pip3 install -user "Your_package"
for example if you wanted to install opencv (cv2 in the above list)
pip3 install -user opencv-python