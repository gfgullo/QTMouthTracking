import cv2
import dlib
import numpy as np
from action import Action
#from beep import Beep
from music import Music

class Camera:

    _OPEN_VALUE = 1.6 # valore della tangente che identifica la bocca aperta
    _CLOSE_VALUE = 1.2 # valore della tangente che identifica la bocca chiusa

    _triggered=False

    def __init__(self):
        self._video_capture = cv2.VideoCapture(1)
        self._detector = dlib.get_frontal_face_detector()

        # link al modello: http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
        self._predictor = dlib.shape_predictor("models/shape_predictor_68_face_landmarks.dat")
        self._music = Music()


    def _rect2bb(self, rect):

        x = rect.left()
        y = rect.top()
        w = rect.right() - x
        h = rect.bottom() - y

        return (x, y, w, h)


    def _shape2np(self, shape, dtype="int"):

        coords = np.zeros((68, 2), dtype=dtype)

        for i in range(0, 68):
            coords[i] = (shape.part(i).x, shape.part(i).y)

        return coords


    def capture(self, detection_enabled, show_rects=False):
        ret, frame = self._video_capture.read()

        if ret:
            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = cv2.resize(img, (640, 480))

            if not detection_enabled:
                return img

            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            rects = self._detector(gray, 1)

            for i, rect in enumerate(rects):

                shape = self._predictor(gray, rect)

                if show_rects:
                    (x, y, w, h) = self._rect2bb(rect)
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    cv2.putText(img, "Face "+str(i+1), (x - 10, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # calcoliamo il coefficiente angolare della retta che passa tra i punti 52 e 49
                m1 = (shape.part(51).x-shape.part(48).x)/(shape.part(51).y-shape.part(48).y+0.0001)

                # calcoliamo il coefficiente angolare della retta che passa tra i punti 57 e 49
                m2 = (shape.part(57).x-shape.part(48).x)/(shape.part(57).y-shape.part(48).y+0.0001)

                # calcoliamo la tangente dell'angolo formato dalle due rette
                tan = (m1-m2)/(1+m1*m2)

                cv2.circle(img, (shape.part(48).x, shape.part(48).y), 1, (0, 0, 255), -1)
                cv2.circle(img, (shape.part(57).x, shape.part(57).y), 1, (0, 0, 255), -1)
                cv2.circle(img, (shape.part(51).x, shape.part(51).y), 1, (0, 0, 255), -1)
                cv2.circle(img, (shape.part(54).x, shape.part(54).y), 1, (0, 0, 255), -1)

                cv2.line(img, (shape.part(48).x, shape.part(48).y), (shape.part(57).x, shape.part(57).y), (0, 0, 255))
                cv2.line(img, (shape.part(48).x, shape.part(48).y), (shape.part(51).x, shape.part(51).y), (0, 255, 0))
                cv2.line(img, (shape.part(57).x, shape.part(57).y), (shape.part(51).x, shape.part(51).y), (255, 0, 0))
                cv2.line(img, (shape.part(54).x, shape.part(48).y), (shape.part(57).x, shape.part(57).y), (0, 0, 255))
                cv2.line(img, (shape.part(54).x, shape.part(48).y), (shape.part(51).x, shape.part(51).y), (0, 255, 0))

                if (not self._triggered) and tan>self._OPEN_VALUE:
                    self._triggered=True
                    print("Bocca aperta")
                    #Beep().play()
                    self._music.play()
                    Action().start()
                elif self._triggered and tan<self._CLOSE_VALUE:
                    self._triggered=False
                    print("Bocca chiusa")
                    self._music.stop()

            return img

        return None


if __name__ == "__main__":

    camera = Camera()

    while True:

        img = camera.capture(True, show_rects=True)
        cv2.imshow("Capture", img)

        if cv2.waitKey(1) == ord("q"):
            break
