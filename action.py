from threading import Thread

class Action(Thread):

   def __init__(self,):
      Thread.__init__(self)

   def run(self):
      print("Input rilevato, fai qualcosa in un altro thread!")
      #...