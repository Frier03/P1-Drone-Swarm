#!/usr/bin/env python
import PySimpleGUI as sg
from time import sleep
from preload import splashScreen

def main():
    #  Create splash screen
    splashScreen(Filename='aau.png', sg=sg)

    # Create layout for main window
    layout = [
        
    ]

    # Create main window
    window = sg.Window('Drone Fleet Management Software', layout, size=(900, 700), finalize=True)

    # Start the application loop
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break
    
    window.close()


if __name__ == '__main__':
    main()