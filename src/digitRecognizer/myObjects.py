# -*- coding: utf-8 -*-

import logging
log = logging.getLogger(__name__)
import os

import numpy as np
import cv2

from PyQt5.QtCore import QThread, QObject
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
from PyQt5.QtGui import QImage
from keras.models import load_model

cur_dir = os.path.dirname(os.path.abspath(__file__))


class MainModel(QObject):
    """DigitRecognizer model class, is file-model based on *Model-View-Controller* pattern
    """

    #signals
    sendCameraView = pyqtSignal(QImage)
    send_original_photo_to_gui = pyqtSignal(QImage)
    send_processed_photo_to_gui = pyqtSignal(QImage)
    send_proccesd_image_to_ML = pyqtSignal(object)

    def __init__(self, **kwds):
        super(QObject, self).__init__(**kwds)
        self.original_image = None
        self.processed_image = None

    @pyqtSlot(object)
    def get_image(self, image):
        """Sets incoming image as original image

        Parameters:
        image (numpy.ndarray): incoming image
        """
        self.original_image = image
        self.prepare_images()


    @pyqtSlot(str)
    def load_image(self, path):
        """Opens image from path and sets
        it as original image

        Parameters:
        image (str): image's path
        """
        if path:
            self.original_image = cv2.imread(path, 1)
            self.prepare_images()

    def prepare_images(self):
        """prepares image for model and sends images to app's gui
        """

        qt_original_image = self.convert_image_to_QTformat(self.original_image)
        self.send_original_photo_to_gui.emit(qt_original_image)

        self.processed_image = self.procces_image(self.original_image)
        qt_processed_image = self.convert_image_to_QTformat(self.processed_image)
        self.send_processed_photo_to_gui.emit(qt_processed_image)

    def convert_image_to_QTformat(self, image):
        """Converts  incoming image to qt format

        Parameters:
        image (numpy.ndarray): image that should be convert

        Returns:
        qt_image (QImage): image converted to qt format
        """
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        convertToQtFormat = QImage(image.data, image.shape[1], image.shape[0], QImage.Format_RGB888)
        qt_image = convertToQtFormat.scaled(500, 375, Qt.KeepAspectRatio)
        return qt_image


    def procces_image(self, image):
        """procces image to be appropriate for machine learning algorithm

        Parameters:
        image (numpy.ndarray): image that should be process

        Returns:
        processed_image (numpy.ndarray): image after processing
        """
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        ret, processed_image = cv2.threshold(image, 75, 255, cv2.THRESH_BINARY_INV)
        return processed_image


    @pyqtSlot(str)
    def savePhoto(self, path):
        """saves photo in incoming path

        Parameters:
        path (str): photo directory
        """
        if self.original_image and path:
            cv2.imwrite(path, self.original_image)

    @pyqtSlot()
    def send_processd_for_prediction(self):
        """resizes image and send it to machine learning algorithm"""
        resized_image  = cv2.resize(self.processed_image, (28, 28))
        self.send_proccesd_image_to_ML.emit(resized_image)


class CameraThread(QThread):
    """Thread implement to extract mdf files without freezing the GUI"""

    # SIGNALS
    send_camera_view_to_gui = pyqtSignal(QImage)
    send_photo_to_model = pyqtSignal(object)

    def __init__(self):
        super(QThread, self).__init__()
        self.cap = cv2.VideoCapture(0)

        self.ret = None
        self.frame = None
        self.readyFrame = QImage
        self.binaryGrayImg = None

    def run(self):
        """Gets view from camera and sends it to view
        """
        while True:
            self.ret, self.frame = self.cap.read()
            if self.ret:
                rgbImage = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
                self.readyFrame = convertToQtFormat.scaled(500, 375, Qt.KeepAspectRatio)
                self.send_camera_view_to_gui.emit(self.readyFrame)

    @pyqtSlot()
    def take_photo(self):
        """Saves current frame and sends it to model
        """
        self.photo = self.frame
        self.send_photo_to_model.emit(self.photo)


class MachineLearningAlgorithm(QObject):

    # signals
    sendPredictedDigit = pyqtSignal(str)

    def __init__(self, **kwds):
        """MImgViewerModel constructor
        """
        super(QObject, self).__init__(**kwds)
        self.model = load_model(os.path.join(cur_dir, 'digitRecognizer.h5'))
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
        pass
        # self.correctDigit = correctDigit
        # y = np.zeros(10)
        # y[int(self.correctDigit)] = 1
        # y = y.reshape(1,10)
        # #print(y)
        # self.model.fit(self.image, y, batch_size=128, epochs=20, verbose=2)
        # self.model.save('digitRecognizer.h5')
        # self.model = load_model('digitRecognizer.h5')
        # #print(self.image.shape)