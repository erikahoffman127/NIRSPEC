import numpy as n
import matplotlib.pyplot as plt

x, y = n.mgrid[range(256)[::11], range(256)[::11]]
x, y = n.ravel(x), n.ravel(y)

dist_x, dist_y = undistorted_to_distorted(x, y)

x_undist, y_undist = distorted_to_undistorted(dist_x, dist_y)

plt.rcParams["figure.figsize"] = (9,9)
plt.scatter(dist_x, dist_y, c= 'blue')
plt.scatter(x, y, c= 'red')
plt.scatter(x_undist, y_undist, 15, c= 'green')
plt.show()
