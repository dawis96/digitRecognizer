import numpy as np
import cv2

from PyQt5.QtCore import QThread, QObject
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QImage
from keras.models import load_model


class CameraView(QThread):

    #signals
    sendCameraView = pyqtSignal(QImage)
    sendCameraFrame = pyqtSignal(QImage)
    sendImageToLabel = pyqtSignal(QImage)
    sendImageToModel = pyqtSignal(object)

    def __init__(self):
        super(QThread, self).__init__()
        self.cap = cv2.VideoCapture(0)

        self.ret = None
        self.frame = None
        self.readyFrame = QImage
        self.binaryGrayImg = None

    def run(self):
        while True:
            self.ret, self.frame = self.cap.read()
            if self.ret:
                rgbImage = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                self.readyFrame = convertToQtFormat.scaled(500, 375, Qt.KeepAspectRatio)
                self.sendCameraView.emit(self.readyFrame)

    @pyqtSlot(int, str)
    def sendPhoto(self, num, path):
        if num == 0:
            self.photo = self.frame
        elif num == 1:
                self.photo = cv2.imread(path, 1)
        try :
            rgbImage = cv2.cvtColor(self.photo, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
            readyFrame2 = convertToQtFormat.scaled(500, 375, Qt.KeepAspectRatio)
            self.sendCameraFrame.emit(readyFrame2)
            self.preprocessedPhoto(self.photo)
        except:
            pass


    def preprocessedPhoto(self, photo):
        grayImg = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
        ret, self.binaryGrayImg = cv2.threshold(grayImg, 75, 255, cv2.THRESH_BINARY_INV)
        #resizedImg = cv2.resize(binaryGrayImg, (28, 28))
        convertToQtFormat = QImage(self.binaryGrayImg, self.binaryGrayImg.shape[1], self.binaryGrayImg.shape[0], QImage.Format_Grayscale8)
        readyFrame3 = convertToQtFormat.scaled(500, 375, Qt.KeepAspectRatio)
        self.sendImageToLabel.emit(readyFrame3)
        # print('a')

    pyqtSlot(str)
    def savePhoto(self, path):
            try:
                cv2.imwrite(path, self.photo)
            except:
                pass


    pyqtSlot()
    def imageToModel(self):
        resized  = cv2.resize(self.binaryGrayImg, (28, 28))
        self.sendImageToModel.emit(resized)


class CnnModel(QObject):

    # signals
    sendPredictedDigit = pyqtSignal(str)

    def __init__(self, **kwds):
        """MImgViewerModel constructor
        """
        super(QObject, self).__init__(**kwds)
        self.model = load_model('digitRecognizer.h5')
        self.image = None
        self.correctDigit = None

    @pyqtSlot(object)
    def takeImage(self, img):
        self.image = img
        self.image = self.image.reshape(1, 784)

        self.predictDigit()

    def predictDigit(self):
        predict = self.model.predict(self.image)
        predict_class = self.model.predict_classes(self.image)
        print(predict)
        print(predict.shape)
        #print(str(predict_class[0]))
        self.sendPredictedDigit.emit(str(predict_class[0]))

    @pyqtSlot(str)
    def improveModel(self, correctDigit):
        self.correctDigit = correctDigit
        y = np.zeros(10)
        y[int(self.correctDigit)] = 1
        y = y.reshape(1,10)
        #print(y)
        self.model.fit(self.image, y, batch_size=128, epochs=20, verbose=2)
        self.model.save('digitRecognizer.h5')
        self.model = load_model('digitRecognizer.h5')
        #print(self.image.shape)