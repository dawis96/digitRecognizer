from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import cv2

class CameraView(QThread):

    #signals
    sendCameraView = pyqtSignal(QImage)
    sendCameraFrame = pyqtSignal(QImage)
    sendImageToLabel = pyqtSignal(QImage)




    def __init__(self):
        super(QThread, self).__init__()
        self.cap = cv2.VideoCapture(0)
        self.startRecording = True  # change to false and add a button to turn on camera
        self.ret = None
        self.frame = None
        self.readyFrame = QImage

    def run(self):
        while self.startRecording:
            self.ret, self.frame = self.cap.read()
            if self.ret:
                rgbImage = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                self.readyFrame = convertToQtFormat.scaled(500, 375, Qt.KeepAspectRatio)
                self.sendCameraView.emit(self.readyFrame)

    @pyqtSlot()
    def sendPhoto(self):
        self.photo = self.frame
        if self.ret:
            rgbImage = cv2.cvtColor(self.photo, cv2.COLOR_BGR2RGB)
            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
            readyFrame2 = convertToQtFormat.scaled(500, 375, Qt.KeepAspectRatio)
            self.sendCameraFrame.emit(readyFrame2)
            #self.sendPhotoToProcess.emit(self.photo)
            self.preprocessedPhoto(self.photo)

    def preprocessedPhoto(self, photo):
        grayImg = cv2.cvtColor(photo, cv2.COLOR_BGR2GRAY)
        ret, binaryGrayImg = cv2.threshold(grayImg, 75, 255, cv2.THRESH_BINARY_INV)
        resizedImg = cv2.resize(binaryGrayImg, (28, 28))


        convertToQtFormat = QImage(binaryGrayImg, binaryGrayImg.shape[1], binaryGrayImg.shape[0], QImage.Format_Grayscale8)
        readyFrame3 = convertToQtFormat.scaled(500, 375, Qt.KeepAspectRatio)
        self.sendImageToLabel.emit(readyFrame3)
        # print('a')





