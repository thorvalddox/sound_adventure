import os

def speak(text):
    os.system("espeak \"{}\"".format(text))