# -*- coding: utf-8 -*-
import os
import sys
import logging
log = logging.getLogger(__name__)

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QWidget
from PyQt5.uic import loadUi

from .myObjects import MainModel, MachineLearningAlgorithm, CameraThread
from .myWidgets import ImagesButtons, ImagesLabels, AiWidget

cur_dir = os.path.dirname(os.path.abspath(__file__))


class DigitRecognizer(QWidget):
    """digitRecognizer class build on MVC Pattern"""

    def __init__(self, **kwds):
        super(QWidget, self).__init__(**kwds)
        """digitRecognizer constructor, define user interface appearance and connections between components of the MVC 
        pattern  """

        #model
        self.model = MainModel()
        self.camera_thread = CameraThread()
        self.machine_learning_algorithm = MachineLearningAlgorithm()


        #view
        self.imageLabels = ImagesLabels()

        #control
        self.imageButtons = ImagesButtons()
        self.aiWidget = AiWidget()

        # user interference setting
        loadUi(os.path.join(cur_dir, "ui/iv.ui"), self)
        self.setWindowTitle("Digit Recognizer ver 0.1")
        #self.resize(1600, 550)
        self.setMinimumSize(1600, 550)
        self.setMaximumSize(1600, 550)
        self.verticalLayout.addWidget(self.imageButtons)
        self.verticalLayout.addWidget(self.imageLabels)
        self.verticalLayout.addWidget(self.aiWidget)

        # connections
        # camera_thread to imageLabels
        self.camera_thread.send_camera_view_to_gui.connect(self.imageLabels.show_camera_view)

        # camera_thread to model
        self.camera_thread.send_photo_to_model.connect(self.model.get_image)

        # model to imageLabels
        self.model.send_original_photo_to_gui.connect(self.imageLabels.show_photo)
        self.model.send_processed_photo_to_gui.connect(self.imageLabels.show_processed_photo)

        # model to machine_learning_algorithm
        self.model.send_proccesd_image_to_ML.connect(self.machine_learning_algorithm.takeImage)

        # machine_learning_algorithm to aiWidget
        self.machine_learning_algorithm.sendPredictedDigit.connect(self.aiWidget.set_prediction_result)

        # imageButtons to camera_thread
        self.imageButtons.takePhoto.connect(self.camera_thread.take_photo)

        # imageButtons to model
        self.imageButtons.sendPhotoDir.connect(self.model.load_image)
        self.imageButtons.savePhoto.connect(self.model.savePhoto)

        # aiWidget to model
        self.aiWidget.predictDigit.connect(self.model.send_processd_for_prediction)

        # aiWidget to cnnmodel
        self.aiWidget.sendCorrectedDigit.connect(self.machine_learning_algorithm.improveModel)

        self.camera_thread.start()

def myExceptionhook(exc_type, exc_value, exc_traceback):
    log.critical("Unexpected exception occurred!",
                 exc_info=(exc_type, exc_value, exc_traceback))

def main():
    # logging.basicConfig(level=logging.DEBUG)
    sys.excepthook = myExceptionhook
    app = QApplication(sys.argv)
    # app.setWindowIcon(QIcon('imgs\icon.png'))
    digitRecognizer = DigitRecognizer()
    digitRecognizer.show()

    sys.exit(app.exec_())

if __name__ == '__main__':

    main()