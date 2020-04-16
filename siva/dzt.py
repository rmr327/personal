from readgssi import readgssi
from matplotlib.pyplot import imshow
from scipy.signal import find_peaks

a, b, c = readgssi.readgssi(infile='/home/rmr327/Desktop/FILE__342.DZT')
peaks, _ = find_peaks(b[0][55], height=0)
print(peaks)

imshow(b[0])
