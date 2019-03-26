import numpy as np
import cv2
import os
from matplotlib import pyplot as plt
from skimage.morphology import extrema
from skimage.morphology import watershed as skwater


def ShowImage(title, img, ctype):
  plt.figure(figsize=(10, 10))
  if ctype == 'bgr':
    b, g, r = cv2.split(img)
    rgb_img = cv2.merge([r, g, b])
    plt.imshow(rgb_img)
  elif ctype == 'hsv':
    rgb = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
    plt.imshow(rgb)
  elif ctype == 'gray':
    plt.imshow(img, cmap='gray')
  elif ctype == 'rgb':
    plt.imshow(img)
  else:
    raise Exception("Unknown colour type")
  plt.axis('off')
  plt.title(title)
  plt.show()

def seg():
  img = cv2.imread('C:/Users/venu/Desktop/VI sem/Self Study/user inputs/1.jpg')

  Z = img.reshape((-1, 3))

  Z = np.float32(Z)

  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TermCriteria_MAX_ITER, 10, 1.0)
  K = 8
  ret, label, center = cv2.kmeans(
      Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

  center = np.uint8(center)
  res = center[label.flatten()]
  res2 = res.reshape((img.shape))
  #ShowImage('1.Cluster', res2, 'gray')
  median = cv2.medianBlur(res2, 5)
  blur = cv2.bilateralFilter(res2, 9, 75, 75)
  #ShowImage('2.Median', blur, 'gray')

  gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)
  ret, thresh = cv2.threshold(
      gray, 0, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)


  kernel = np.ones((3, 3), np.uint8)
  opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

  sure_bg = cv2.dilate(opening, kernel, iterations=3)

  dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
  ret, sure_fg = cv2.threshold(dist_transform, 0.7*dist_transform.max(), 255, 0)

  sure_fg = np.uint8(sure_fg)
  unknown = cv2.subtract(sure_bg, sure_fg)


  ret, markers = cv2.connectedComponents(sure_fg)

  markers = markers+1


  markers[unknown == 255] = 0
  markers = cv2.watershed(img, markers)
  img[markers == -1] = [255, 0, 0]

  im1 = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
  #ShowImage('3.Watershed Segmented', im1, 'gray')

  Z = im1.reshape((-1, 3))

  Z = np.float32(Z)

  criteria = (cv2.TERM_CRITERIA_EPS + cv2.TermCriteria_MAX_ITER, 10, 1.0)
  K = 3
  ret, label, center = cv2.kmeans(
      Z, K, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

  center = np.uint8(center)
  res = center[label.flatten()]
  res2 = res.reshape((img.shape))
  #ShowImage('4.Clusterfinal', res2, 'gray')


  path = 'C:/Users/venu/Desktop/VI sem/Self Study/static/images/'
  cv2.imwrite(os.path.join(path, 'final.jpg'), res2)

  im = cv2.imread('C:/Users/venu/Desktop/VI sem/Self Study/static/images/final.jpg')


  fromCenter = False
  r = cv2.selectROI(im, fromCenter)

  imCrop = im[int(r[1]):int(r[1]+r[3]), int(r[0]):int(r[0]+r[2])]


  #cv2.imshow("Image", imCrop)
  path = 'C:/Users/venu/Desktop/VI sem/Self Study/user inputs/'
  cv2.imwrite(os.path.join(path, '1f.jpg'), imCrop)

  image = cv2.imread('C:/Users/venu/Desktop/VI sem/Self Study/user inputs/1f.jpg')
  height = np.size(image, 0)
  width = np.size(image, 1)
  height= height*0.26458
  width= width*0.26458

  print('width is %d and height is %d' % (width, height))
  return ((width,height))

