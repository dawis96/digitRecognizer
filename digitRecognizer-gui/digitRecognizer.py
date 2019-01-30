from myObjects import *
from myWidgets import *

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
        self.camera.sendCameraView.connect(self.imageLabels.setCameraLabel)
        self.camera.sendCameraFrame.connect(self.imageLabels.setPhotoLabel)
        self.camera.sendImageToLabel.connect(self.imageLabels.setImageLabel)

        # camera to cnnmodel
        self.camera.sendImageToModel.connect(self.cnnmodel.takeImage)

        #cnnmodel to aiWidget
        self.cnnmodel.sendPredictedDigit.connect(self.aiWidget.setText)

        # imageButtons to camera
        self.imageButtons.takephoto.connect(self.camera.sendPhoto)
        self.imageButtons.sendPhotoDir.connect(self.camera.sendPhoto)
        self.imageButtons.savePhoto.connect(self.camera.savePhoto)

        # aiWidget to camera
        self.aiWidget.predictDigit.connect(self.camera.imageToModel)

        self.camera.start()
        #self.camera.startRecording = True
        #self.camera.start()




if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    #app.setWindowIcon(QIcon('imgs\icon.png'))
    digitRecognizer = DigitRecognizer()
    digitRecognizer.show()

    sys.exit(app.exec_())