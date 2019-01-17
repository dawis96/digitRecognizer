import cv2
from keras.models import  load_model

img = cv2.imread('digit8.jpg', 0)
cv2.imshow('digit', img)

print(img.shape)
readyimg = img.reshape(1, 784)
print(readyimg.shape)

mnist_model = load_model('digitRecognizer.h5')

predicted_classes = mnist_model.predict(readyimg)

for i in range(len(predicted_classes[0])):
    if predicted_classes[0][i]:
        print('AI: I think that is '+str(i))
        
if cv2.waitKey(0):
    cv2.destroyAllWindows()