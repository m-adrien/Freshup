# -*-coding:Latin-1 -*
import os
import sys
#from random import random
import threading
#import time
#
#result = None
#print("Bonjour le monde !")
#os.system("pause")
#
#def background_calculation():
#    os.system('C:\CS.exe')
#def main():
#    thread = threading.Thread(target=background_calculation)
#    thread.start()
#
#    # wait here for the result to be available before continuing
#    thread.join()
#
#    print('The programm is done')
#
#if __name__ == '__main__':
#    main()


print('Iptables-persistent setup...\n')


def iptables_install():
    """Setup iptable-persistent on linux distribution which have aperture"""
    os.system('C:\CS.exe')


def main():  # Attente de la fin d'installation mis en thread par la fonction main
    thread = threading.Thread(target=iptables_install)
    thread.start()
    thread.join()
if __name__ == '__main__':
    main()
print('done.\n')