# -*-coding:Latin-1 -*
import os
from random import random
import threading
import time

result = None
print("Bonjour le monde !")
os.system("pause")

def background_calculation():
    os.system('C:\CS.exe')
def main():
    thread = threading.Thread(target=background_calculation)
    thread.start()

    # wait here for the result to be available before continuing
    thread.join()

    print('The programm is done')

if __name__ == '__main__':
    main()