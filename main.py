#!/usr/bin/env python
import PySimpleGUI as sg
from time import sleep

def splashScreen(Filename = None) -> None:
    if Filename is None:
        raise TypeError("No image provided")
    
    # Change display time so instead we will be loading all necessary modules and test before displaying main window
    TIMEOUT_SECONDS = 4000

    # Create splash screen window
    sg.Window('SS', [[sg.Image(Filename)]], transparent_color=sg.theme_background_color(), no_titlebar=True, keep_on_top=True).read(timeout=TIMEOUT_SECONDS, close=True)

splashScreen(Filename = 'aau.png')

def Setup() -> None:
    layout = [
        [sg.Text('Drone Fleet Management Software')]
        ]

    # Create new window
    window = sg.Window('Drone Fleet Management Software | AAU - P1', layout)
    return window

window = Setup()

def Loop(window) -> None:
    while True:
        event, values = window.read()

        if event == sg.WIN_CLOSED:
            break

Loop(window)

window.close()