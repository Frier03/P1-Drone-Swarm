import atexit
from time import sleep

class idk:
    def run(self):
        for i in range(10):
            sleep(0.1)
            print("looping")
            if i == 10:
                a = 1 / 0
    def __delattr__(self, __name: str):
        print("im deleted")

def exitHandler():
    print("EXITING")

atexit.register(exitHandler)

i = idk()
i.run()
del i

