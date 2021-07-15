from PyQt5.QtCore import *
from PyQt5.QtGui import *
from camera import Camera

class Worker(QThread):

    update_img = pyqtSignal(QImage)
    enabled = False

    def run(self):

        self.active = True
        camera = Camera()

        while self.active:
            img = camera.capture(self.enabled)
            qtimg = QImage(img.data, img.shape[1], img.shape[0], QImage.Format_RGB888)
            self.update_img.emit(qtimg)

    def stop(self):
        self.active = False
        self.quit()