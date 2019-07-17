import pyautogui
try:
    while True:
        x, y = pyautogui.position()
        print(x,y)
except KeyboardInterrupt:
    print('\nExit.')
