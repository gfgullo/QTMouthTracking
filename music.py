import pygame
from time import sleep
from threading import Thread

class Music:

    def __init__(self, volume=0.2):
        pygame.mixer.init()
        self._music = pygame.mixer.Sound("resources/pokerface.mp3")
        self._music.set_volume(volume)
        self.playing = False
        self.thr = None

    def play(self):
        self.thr = Thread(target=self._play)
        self.thr.start()

    def _play(self):
        self._music.play()
        self.playing=True
        while self.playing: #pygame ha bisogno di un loop per eseguire l'audio
            pygame.time.delay(100)
        pygame.mixer.pause() #quando playing è false sospendiamo l'audio

    def stop(self):
        if self.thr==None:
            print("No thread started!")
        else:
            self.playing=False


if __name__=="__main__":

    music = Music()
    music.play()
    sleep(4)
    music.stop()