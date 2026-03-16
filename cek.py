from math import pi
import matplotlib.pyplot as plt

result = 0
sign = 1

x = range(1, 200, 2)
y = list()

for denom in x:
    result += sign * (1 / denom)
    y.append(result * 4)
    sign *= -1

fig, ax = plt.subplots()
ax.grid(True)
ax.plot(x, y)
ax.hlines(y=pi, xmin=1, xmax=list(x)[-1], linewidth=2, color='r')

plt.show()

plt.show()
