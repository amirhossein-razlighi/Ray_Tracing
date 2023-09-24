import numpy as np
import matplotlib.pyplot as plt

width = 300
height = 200

camera = np.array([0, 0, 1])
ratio = 1.0 * width / height
screen = (-1, 1.0 / ratio, 1, -1.0 / ratio)  # left, top, right, bottom

image = np.zeros((height, width, 3))

x, y = np.meshgrid(
    np.linspace(screen[0], screen[2], width), np.linspace(screen[1], screen[3], height)
)

for i in range(height):
    for j in range(width):
        # image[i, j] = ...
        print("progress: %d/%d" % (i + 1, height))

plt.imshow(image)
plt.show()
