from PyQt5.QtWidgets import *
from PyQt5.uic import loadUi
import PyQt5.QtGui as QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import pyqtSignal, pyqtSlot, Qt
import urllib.request

class ImagesLabels(QLabel):
    """Camera, photo and processed image display widget"""
    def __init__(self, **kwds):
        super(QLabel, self).__init__(**kwds)
        """ImagesLabel constructor
        """
        loadUi("ui/imagesPanel.ui", self)
        self.cameraLabel.setScaledContents(True)
        self.photoLabel.setScaledContents(True)
        self.imageLabel.setScaledContents(True)

    @pyqtSlot(QImage)
    def setCameraLabel(self, image):
        self.cameraLabel.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(QImage)
    def setPhotoLabel(self, image):
        self.photoLabel.setPixmap(QPixmap.fromImage(image))
        #self.photoLabel.setText(image)


    @pyqtSlot(QImage)
    def setImageLabel(self, image):
        self.imageLabel.setPixmap(QPixmap.fromImage(image))
        # self.photoLabel.setText(image)


class ImagesButtons(QWidget):

    takephoto = pyqtSignal()

    def __init__(self, **kwds):
        super(QWidget, self).__init__(**kwds)
        """OpenSaveWidget constructor"""

        loadUi("ui/imagesControlPanel.ui", self)
        self.status = 'stop'

        #set icons


        #connections

        self.photoButton.clicked.connect(self.takePhotoClicked)
        # self.openButton.clicked.connect(self.choseImageClicked)

    def takePhotoClicked(self):
        self.takephoto.emit()














# if __name__ == '__main__':
#     import sys
#     app = QApplication(sys.argv)
#     widget = ImagesButtons()
#     widget.show()
#     sys.exit(app.exec_())