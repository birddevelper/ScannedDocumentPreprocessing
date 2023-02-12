
import cv2
import numpy as np
import math



def get_angle(x1, y1, x2, y2) -> float:
    """Get the angle of this line with the horizontal axis."""
    deltaX = x2 - x1
    deltaY = y2 - y1
    angleInDegrees = np.arctan2(deltaY , deltaX) * 180 / math.pi
    
    return angleInDegrees

def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR, borderValue=(255,255,255) )
    return result


def align_image(img):

    # Median blurring to get rid of the noise; invert image
    #img =  cv2.medianBlur(img, 3) # use this if the document image is noisy

    edges = cv2.Canny(img, 80, 120)

    # Detect and draw lines
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 10, minLineLength=20, maxLineGap=15)
    # sort lines from widest to shortest
    lines = sorted(lines,key = (lambda l: abs(l[0][0]-l[0][2])) , reverse = True)

    # if there exist any line, compare it by horizontal line
    # and rotate the image if the angle difference is more than 0.25
    for line in lines:
        for x1, y1, x2, y2 in line:
            if (abs(x2-x1) / edges.shape[1])>0.25 :
                print(x1,x2)
                angle = get_angle(x1, y1, x2, y2)
                if abs(angle) > 1.0 :
                    img = rotate_image(img,angle)
                    print("rotated")
        #exit after comparing widest line
        break

    return img