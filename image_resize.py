import numpy as np
from skimage.transform import resize

def resize_images(images, size):
  """Resizes images to the given size.

  Args:
    images: A numpy array of images.
    size: The target size of the images.

  Returns:
    A numpy array of resized images.
  """

  resized_images = np.zeros((images.shape[0], size[0], size[1], images.shape[3]))
  for i in range(images.shape[0]):
    resized_images[i] = resize(images[i], size, order=3)
  return resized_images

