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
        """Sets frames from camera on cameraLabel"""
        self.cameraLabel.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(QImage)
    def setPhotoLabel(self, image):
        """Sets photo to processes on photoLabel"""
        self.photoLabel.setPixmap(QPixmap.fromImage(image))

    @pyqtSlot(QImage)
    def setImageLabel(self, image):
        """Sets processed photo on imageLabel"""
        self.imageLabel.setPixmap(QPixmap.fromImage(image))


class ImagesButtons(QWidget):

    # pyqt signals
    takephoto = pyqtSignal(int, str)
    sendPhotoDir = pyqtSignal(int, str)
    savePhoto = pyqtSignal(str)

    def __init__(self, **kwds):
        super(QWidget, self).__init__(**kwds)
        """OpenSaveWidget constructor"""

        loadUi("ui/imagesControlPanel.ui", self)
        self.status = 'stop'

        #set icons
        icon = QtGui.QIcon("imgs/photo")
        self.openButton.setIcon(icon)
        icon = QtGui.QIcon("imgs/save")
        self.saveButton.setIcon(icon)
        icon = QtGui.QIcon("imgs/takePhoto")
        self.photoButton.setIcon(icon)

        #connections

        self.photoButton.clicked.connect(self.takePhotoClicked)
        self.openButton.clicked.connect(self.choseImageClicked)
        self.saveButton.clicked.connect(self.saveImageClicked)

    def takePhotoClicked(self):
        """Photo button clicked event handler"""
        self.takephoto.emit(0, '')

    def choseImageClicked(self):
        """Open button clicked event handler"""
        window_title = "Select Photo"
        path = str(QFileDialog.getOpenFileName(self, window_title, '', "Image files (*.jpg *.jpeg *.png)"))
        path = path.split(',')
        path = path[0][1:]
        path = path.replace('/', '\\', 1)
        path = path[1:-1]
        self.sendPhotoDir.emit(1, path)

    def saveImageClicked(self):
        """Save button clicked event handler"""
        window_title = "Save Photo"
        path = str(QFileDialog.getSaveFileName(self, window_title, '', "Image files (*.jpg *.jpeg *.png)"))
        path = path.split(',')
        path = path[0][1:]
        path = path.replace('/', '\\', 1)
        path = path[1:-1]
        self.savePhoto.emit(path)


class AiWidget(QWidget):

    # signals
    predictDigit = pyqtSignal()
    sendTrueDigit = pyqtSignal(str)

    def __init__(self, **kwds):
        super(QWidget, self).__init__(**kwds)
        """OpenSaveWidget constructor"""

        loadUi("ui/aiPanel.ui", self)
        self.status = 'stop'

        #set icons
        icon = QtGui.QIcon("imgs/ai")
        self.predictButton.setIcon(icon)
        icon = QtGui.QIcon("imgs/true")
        self.trueButton.setIcon(icon)
        icon = QtGui.QIcon("imgs/false")
        self.falseButton.setIcon(icon)

        #connections

        self.predictButton.clicked.connect(self.predictClicked)
        self.trueButton.clicked.connect(self.goodPredictionClicked)
        self.falseButton.clicked.connect(self.badPredictionClicked)
        # label -> aiLabel

        self.prediction = 0


    def predictClicked(self):
        """predict button clicked event handler"""
        self.predictDigit.emit()

    @pyqtSlot(str)
    def setText(self, digit):
        """sets dialogue with predicted digit on aiLabel"""
        self.prediction = digit
        self.aiLabel.setText("AI: It is "+self.prediction+", isn't it?")

    def goodPredictionClicked(self):
        """true prediction button clicked event handler"""
        print(self.prediction)
        self.sendTrueDigit.emit(str(self.prediction))

    def badPredictionClicked(self):
        text, okPressed = QInputDialog.getText(self, "enter digit", "Enter Correct digit", QLineEdit.Normal, "")
        if okPressed and text != '':
            try:
                self.sendTrueDigit.emit(text)
            except:
                pass










if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    widget = AiWidget()
    widget.show()
    sys.exit(app.exec_())