import cv2
from keras.models import  load_model
import numpy as np 

cap = cv2.VideoCapture(0)

def cameraView():
    """ shows frames from camera"""
    ret, frame = cap.read()
    cv2.imshow('camera view', frame)
    return frame

def takePhoto(frame):
    """ takes frame from camera view and saves it"""
    cv2.imwrite('photo.jpg', frame)
    takenPhoto = cv2.imread('photo.jpg')
    print(takenPhoto.shape)
    preprocesingPhoto(takenPhoto)
    cv2.imshow('taken photo', takenPhoto)
       
def preprocesingPhoto(image):
    """Pre=procesing photo to image that can be read by neural network model"""
    # converting photo to gray scale
    grayImg = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # converting grayscale image to binary
   # thresh, binaryGrayImg = cv2.threshold(grayImg, 200, 255, cv2.THRESH_BINARY |
                                            #cv2.THRESH_OTSU)
    ret,binaryGrayImg = cv2.threshold(grayImg,75,255,cv2.THRESH_BINARY_INV)                                        
# =============================================================================
#     binaryGrayImg = cv2.adaptiveThreshold(grayImg,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
#                 cv2.THRESH_BINARY,11,2)
# =============================================================================
# =============================================================================
#     binaryGrayImg = cv2.adaptiveThreshold(grayImg ,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
#                                 cv2.THRESH_BINARY,11,2)
# =============================================================================
    resizedImg = cv2.resize(binaryGrayImg, (28,28))
    #preprocesedImg = 255 - resizedImg
# =============================================================================
#     cv2.imshow('preprocesed photo', cv2.resize(resizedImg,(280,280)))
# =============================================================================
    cv2.imshow('preprocesed photo', binaryGrayImg)
    recognizingDigit(resizedImg)
    
def recognizingDigit(image):
    readyImg = image.reshape(1, 784)
    mnist_model = load_model('digitRecognizer.h5')
    pre = mnist_model.predict_classes(readyImg)
    predicted_classes = mnist_model.predict(readyImg)


    print(predicted_classes)
    print(pre)
    for i in range(len(predicted_classes[0])):
        if predicted_classes[0][i]:
            print('AI: I think it is '+str(i))



print('press "p" to take a photo or "q" to quit')
while True:
    frame = cameraView()
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('p'):
        takePhoto(frame)
        print('press "p" to take a photo or "q" to quit')
        
cap.release()
cv2.destroyAllWindows()


