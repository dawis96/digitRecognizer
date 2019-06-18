# -*- coding: utf-8 -*-
import os
import sys
import logging
log = logging.getLogger(__name__)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

from myObjects import CameraView, CnnModel
from myWidgets import ImagesButtons, ImagesLabels, AiWidget

class DigitRecognizer(QWidget):
    """digitRecognizer class build on MVC Pattern"""

    def __init__(self, **kwds):
        super(QWidget, self).__init__(**kwds)
        """digitRecognizer constructor, define user interface appearance and connections between components of the MVC 
        pattern  """

        #model
        self.camera = CameraView()
        self.cnnmodel = CnnModel()


        #view
        self.imageLabels = ImagesLabels()

        #control
        self.imageButtons = ImagesButtons()
        self.aiWidget = AiWidget()

        # user interference setting
        loadUi("ui/iv.ui", self)
        self.setWindowTitle("Digit Recognizer ver 0.1")
        #self.resize(1600, 550)
        self.setMinimumSize(1600, 550)
        self.setMaximumSize(1600, 550)
        self.verticalLayout.addWidget(self.imageButtons)
        self.verticalLayout.addWidget(self.imageLabels)
        self.verticalLayout.addWidget(self.aiWidget)

        # connections
        # camera to imageLabels
        self.camera.sendCameraView.connect(self.imageLabels.show_camera_view)
        self.camera.sendCameraFrame.connect(self.imageLabels.show_photo)
        self.camera.sendImageToLabel.connect(self.imageLabels.show_processed_photo)

        # camera to cnnmodel
        self.camera.sendImageToModel.connect(self.cnnmodel.takeImage)

        #cnnmodel to aiWidget
        self.cnnmodel.sendPredictedDigit.connect(self.aiWidget.set_prediction_result)

        # imageButtons to camera
        self.imageButtons.takePhoto.connect(self.camera.sendPhoto)
        self.imageButtons.sendPhotoDir.connect(self.camera.sendPhoto)
        self.imageButtons.savePhoto.connect(self.camera.savePhoto)

        # aiWidget to camera
        self.aiWidget.predictDigit.connect(self.camera.imageToModel)

        # aiWidget to cnnmodel
        self.aiWidget.sendCorrectedDigit.connect(self.cnnmodel.improveModel)

        self.camera.start()
        #self.camera.startRecording = True
        #self.camera.start()

def myExceptionhook(exc_type, exc_value, exc_traceback):
    log.critical("Unexpected exception occurred!",
                 exc_info=(exc_type, exc_value, exc_traceback))

if __name__ == '__main__':

    # logging.basicConfig(level=logging.DEBUG)
    sys.excepthook = myExceptionhook
    app = QApplication(sys.argv)
    #app.setWindowIcon(QIcon('imgs\icon.png'))
    digitRecognizer = DigitRecognizer()
    digitRecognizer.show()

    sys.exit(app.exec_())