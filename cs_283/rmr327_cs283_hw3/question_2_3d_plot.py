from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt


fig = plt.figure()
ax = plt.axes(projection='3d')


def f(xx, yy):
    return (xx + yy - 2)**2


x = np.linspace(-20, 20, 1000)
y = np.linspace(-20, 20, 1000)

X, Y = np.meshgrid(x, y)
Z = f(X, Y)

ax.plot_surface(X, Y, Z, edgecolor='none')
ax.set_title(' x vs y, vs g(x,y)')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('g(x,y)')

plt.show()
