# -*- coding: utf-8 -*-
import os
import logging
log = logging.getLogger(__name__)

from PyQt5.QtWidgets import QLabel, QWidget, QFileDialog, QInputDialog, QLineEdit
from PyQt5.uic import loadUi
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtCore import pyqtSignal, pyqtSlot

cur_dir = os.path.dirname(os.path.abspath(__file__))


class ImagesLabels(QLabel):
    """Widget to dispaly camera view, taken/loaded photo and processed image."""

    def __init__(self, **kwds):
        super(QLabel, self).__init__(**kwds)
        """ImagesLabel constructor
        """
        loadUi(os.path.join(cur_dir, "ui/imagesPanel.ui"), self)
        self.cameraLabel.setScaledContents(True)
        self.photoLabel.setScaledContents(True)
        self.imageLabel.setScaledContents(True)

    @pyqtSlot(QImage)
    def show_camera_view(self, frame):
        """Sets camera view on cameraLabel

        Parameters:
        frame (QImage): single frame from camera
        """
        self.cameraLabel.setPixmap(QPixmap.fromImage(frame))

    @pyqtSlot(QImage)
    def show_photo(self, image):
        """Sets photo to processes on photoLabel

        Parameters:
        image (QImage): taken/loaded image
        """
        self.photoLabel.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(QImage)
    def show_processed_photo(self, image):
        """Sets processed photo on imageLabel

        Parameters:
        image (QImage): taken/loaded image after processing
        """
        self.imageLabel.setPixmap(QPixmap.fromImage(image))


class ImagesButtons(QWidget):
    """Widget with three buttons correspond to load existing photo, take photo using camera, save taken photo
    """

    # pyqt signals
    takePhoto = pyqtSignal(int, str)
    sendPhotoDir = pyqtSignal(int, str)
    savePhoto = pyqtSignal(str)

    def __init__(self, **kwds):
        super(QWidget, self).__init__(**kwds)
        """OpenSaveWidget constructor"""

        loadUi(os.path.join(cur_dir, "ui/imagesControlPanel.ui"), self)
        self.status = 'stop'

        #set icons
        icon = QIcon(os.path.join(cur_dir, "icons/photo"))
        self.openButton.setIcon(icon)
        icon = QIcon(os.path.join(cur_dir, "icons/save"))
        self.saveButton.setIcon(icon)
        icon = QIcon(os.path.join(cur_dir, "icons/takePhoto"))
        self.photoButton.setIcon(icon)

        #connections
        self.photoButton.clicked.connect(self.take_photo_clicked)
        self.openButton.clicked.connect(self.chose_image_clicked)
        self.saveButton.clicked.connect(self.save_image_clicked)

        #toolTips
        self.photoButton.setToolTip('Take a photo')
        self.openButton.setToolTip('Load existing photo')
        self.saveButton.setToolTip('Save taken photo')

    def take_photo_clicked(self):
        """Photo button clicked event handler
        """
        self.takePhoto.emit(0, '')

    def chose_image_clicked(self):
        """Open button clicked event handler,
        sends chosen path to model
        """
        window_title = "Select Photo"
        path, _ = QFileDialog.getOpenFileName(self, window_title, '', "Image files (*.jpg *.jpeg *.png)")
        self.sendPhotoDir.emit(1, path)

    def save_image_clicked(self):
        """Save button clicked event handler,
        sends chosen path to model
        """
        window_title = "Save Photo"
        path, _ = QFileDialog.getSaveFileName(self, window_title, '', "Image files (*.jpg *.jpeg *.png)")
        self.savePhoto.emit(path)


class AiWidget(QWidget):
    """Widget calls neural network to predict digit and displays result"""

    # signals
    predictDigit = pyqtSignal()
    sendCorrectedDigit = pyqtSignal(str)

    def __init__(self, **kwds):
        super(QWidget, self).__init__(**kwds)
        """OpenSaveWidget constructor"""

        loadUi(os.path.join(cur_dir, "ui/aiPanel.ui"), self)
        self.status = 'stop'

        #set icons
        icon = QIcon(os.path.join(cur_dir, "icons/ai"))
        self.predictButton.setIcon(icon)
        icon = QIcon(os.path.join(cur_dir, "icons/true"))
        self.trueButton.setIcon(icon)
        icon = QIcon(os.path.join(cur_dir, "icons/false"))
        self.falseButton.setIcon(icon)

        #connections
        self.predictButton.clicked.connect(self.predict_clicked)
        self.trueButton.clicked.connect(self.correct_prediction_clicked)
        self.falseButton.clicked.connect(self.wrong_prediction_clicked)
        # label -> aiLabel

        # toolTips
        self.predictButton.setToolTip('Call AI to predict the number')
        self.trueButton.setToolTip('Confirm of correct detection')
        self.falseButton.setToolTip('Notify wrong detection')

        self.prediction = ''

    def predict_clicked(self):
        """predict button clicked event handler
        """
        self.predictDigit.emit()

    @pyqtSlot(str)
    def set_prediction_result(self, digit):
        """displays prediction result

        Parameters:
        digit (str): digit predicted by machine learning algorithm base on photo
        """
        self.prediction = digit
        self.aiLabel.setText("AI: It is "+self.prediction+", isn't it?")

    def correct_prediction_clicked(self):
        """confirmation of correct detection button clicked event handler
        """
        if self.prediction:
            self.sendCorrectedDigit.emit(str(self.prediction))

    def wrong_prediction_clicked(self):
        """ notification of wrong detection button clicked event handler
        """
        if self.prediction:
            text, ok_pressed = QInputDialog.getText(self, "enter digit", "Enter correct digit:", QLineEdit.Normal, "")
            if ok_pressed and text != '' and str.isdigit(text):
                self.sendCorrectedDigit.emit(text)


