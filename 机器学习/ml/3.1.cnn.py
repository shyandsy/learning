import cv2
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

filter = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]]
weight  = 1
for x in range(1, size_x-1):
  for y in range(1, size_y-1):
      output_pixel = 0.0
      output_pixel = output_pixel + (i[x - 1, y-1] * filter[0][0])
      output_pixel = output_pixel + (i[x, y-1] * filter[0][1])
      output_pixel = output_pixel + (i[x + 1, y-1] * filter[0][2])
      output_pixel = output_pixel + (i[x-1, y] * filter[1][0])
      output_pixel = output_pixel + (i[x, y] * filter[1][1])
      output_pixel = output_pixel + (i[x+1, y] * filter[1][2])
      output_pixel = output_pixel + (i[x-1, y+1] * filter[2][0])
      output_pixel = output_pixel + (i[x, y+1] * filter[2][1])
      output_pixel = output_pixel + (i[x+1, y+1] * filter[2][2])
      output_pixel = output_pixel * weight
      if(output_pixel<0):
        output_pixel=0
      if(output_pixel>255):
        output_pixel=255
      i_transformed[x, y] = output_pixel

# 输出卷积之后的图片
plt.gray()
plt.grid(False)
plt.figure(2)
plt.imshow(i_transformed)
#plt.axis('off')
plt.show()