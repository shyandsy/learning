# pooling 池化
import numpy as np
from scipy import misc
import matplotlib.pyplot as plt

i = misc.ascent()

plt.grid(False)
plt.gray()
plt.axis('on')
plt.figure(1)
plt.imshow(i)


# 用numpy存储图片
i_transformed = np.copy(i)
size_x = i_transformed.shape[0]
size_y = i_transformed.shape[1]

# 输出图像宽和高
print(size_x)
print(size_y)

# 池化
new_x = int(size_x / 2)
new_y = int(size_y / 2)
newImage = np.zeros((new_x, new_y))
for x in range(0, size_x, 2):
    for y in range(0, size_y, 2):
        pixels = []
        pixels.append(i_transformed[x, y])
        pixels.append(i_transformed[x + 1, y])
        pixels.append(i_transformed[x, y + 1])
        pixels.append(i_transformed[x + 1, y + 1])
        pixels.sort(reverse=True)
        newImage[int(x / 2), int(y / 2)] = pixels[0]


# 输出卷积之后的图片
plt.gray()
plt.grid(False)
plt.figure(2)
plt.imshow(newImage)
#plt.axis('off')
plt.show()