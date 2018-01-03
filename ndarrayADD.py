import numpy as np
import matplotlib.pyplot as plt


def f(x):
    return 1.13*x*x + 0.5*x


x = np.linspace(-2*np.pi, 2*np.pi, 50)

reg = np.polyfit(x, f(x), deg=1)
ry = np.polyval(reg, x)

matrix = np.zeros((4, len(x)))
matrix[3, :] = np.sin(x)
matrix[2, :] = x ** 2
matrix[1, :] = x
matrix[0, :] = 1
reg = np.linalg.lstsq(matrix.T, f(x))[0]
ry2 = np.dot(reg, matrix)


plt.plot(x, f(x), 'b', label='f(x)')
plt.plot(x, ry, 'r.', label='regression')
plt.plot(x, ry2, 'k.', label='regression2')
plt.legend(loc=0)
plt.grid(True)
plt.xlabel('x')
plt.ylabel('y')
plt.show()
