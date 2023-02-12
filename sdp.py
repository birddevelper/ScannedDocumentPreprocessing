import cv2
import numpy as np
from image_align import align_image
#read the noisy image
noisyImage= cv2.imread("doc.jpg",cv2.IMREAD_GRAYSCALE)

#applying fast non-local means denoisong filter
denoisedImage= cv2.fastNlMeansDenoising(noisyImage, None, h = 44, templateWindowSize  = 7, searchWindowSize = 21)

## Second step
# binarization with OTSU threshold finder. 0 and 255 are ignored
threshValue, binaryImage = cv2.threshold(denoisedImage, 0, 255, cv2.THRESH_OTSU)

# Third step
#apply re-aligning function
aligned_image = align_image(binaryImage)


before_after = np.concatenate((noisyImage, aligned_image), axis=1)
#save joined images in file
cv2.imwrite("before_after.jpg",before_after)