import matplotlib.pyplot as plt
import numpy as np

x = np.random.randn(60)
y = np.random.randn(60)
print(y)
plt.scatter(x, y, s=80, facecolors='none', edgecolors='r')
plt.show()