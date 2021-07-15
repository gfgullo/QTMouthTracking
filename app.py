from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from worker import Worker


class App(QWidget):
    _dummy = False

    def __init__(self, dummy=False):
        super(App, self).__init__()

        self._dummy = dummy
        self.box_layout = QVBoxLayout()

        self.feed_label = QLabel()
        self.box_layout.addWidget(self.feed_label)

        self.btn_cancel = QPushButton("Enable")

        self.box_layout.addWidget(self.btn_cancel)
        self.feed_label.setPixmap(QPixmap("resources/logo.jpg"))

        if dummy:
            self.feed_label.setPixmap(QPixmap("resources/dummy_img.jpg"))
        else:

            self.btn_cancel.clicked.connect(self.switch_state)

            self.worker = Worker()

            self.worker.start()
            self.worker.update_img.connect(self.update_img_slot)

        self.setLayout(self.box_layout)

    def update_img_slot(self, img):
        self.feed_label.setPixmap(QPixmap.fromImage(img))

    def switch_state(self):
        self.worker.enabled = not self.worker.enabled
        self.btn_cancel.setText("Disable" if self.worker.enabled else "Enable")


    def cancel_feed(self):
        self.worker.stop()


if __name__ == "__main__":
    from PyQt5.QtWidgets import QApplication
    import sys

    qapp = QApplication(sys.argv)
    app = App(dummy=True)
    app.show()
    sys.exit(qapp.exec())