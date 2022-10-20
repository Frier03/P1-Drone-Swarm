def splashScreen(Filename = None, sg=None) -> None:
    if Filename is None:
        raise TypeError("No image provided")
    if sg is None:
        raise TypeError("No PySimpleGUI instance provided")
    
    # Change display time so instead we will be loading all necessary modules and test before displaying main window
    TIMEOUT_SECONDS = 4000

    # Create splash screen window
    sg.Window('SS', [[sg.Image(Filename)]], transparent_color=sg.theme_background_color(), no_titlebar=True, keep_on_top=True).read(timeout=TIMEOUT_SECONDS, close=True)