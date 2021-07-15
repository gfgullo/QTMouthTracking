from threading import Thread
from playsound import playsound

class Beep:

    def play(self):
        thr = Thread(target=self._play, args=(), kwargs={"sound_file":"resources/beep.wav"})
        thr.start()

    def _play(self, sound_file=None):
        playsound(sound_file)


