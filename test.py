import cv2
from keras.models import  load_model

img = cv2.imread('digit2_test.jpg', 0)
cv2.imshow('digit', img)
if cv2.waitKey(0):
    cv2.destroyAllWindows()
print(img.shape)
readyimg = img.reshape(1, 784)
print(readyimg.shape)

mnist_model = load_model('digitRecognizer.h5')

predicted_classes = mnist_model.predict(readyimg)