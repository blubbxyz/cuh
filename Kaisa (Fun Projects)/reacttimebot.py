import pyautogui
print("make sure zour screen is full hd and that you browser is fullscreened")
if input("Press enter to continue...") == "":
    pass
pyautogui.click(921, 639)
while True:
    if pyautogui.pixel(452, 297) == (75, 219, 106):
        pyautogui.click(452, 297)
        print("I see green!!!")
        break
    else:
        print("I see something else")
