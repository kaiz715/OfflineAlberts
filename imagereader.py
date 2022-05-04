#most likely don't need though

import cv2
import os
import keyboard
import time

# def onkeypress(event):
#     print(event.name)

# keyboard.on_press(onkeypress)

# #Use ctrl+c to stop
# while True:
#     if keyboard.is_pressed("delete"):   #if "delete" is pressed, end program
#         break

files = os.listdir("images")

x = 0
for j in files:
    x = x + 1
    print(f"{x} | {j}")
problemSet = int(input("Which problem set: ")) - 1
questionSet = os.listdir(f"images\\{files[problemSet]}")

for k in range(len(questionSet)):
    path = f"images\\{files[problemSet]}\\{questionSet[k]}"
    try:
        img = cv2.imread(path)
        cv2.imshow(questionSet[k],img)   #shows image with its title
        if keyboard.is_pressed("delete"):   #if "delete" is pressed, end program
            break
        cv2.waitKey(0)  #waits until key is pressed to close window
        cv2.destroyAllWindows()
    except Exception as e:
        print(e)
        continue