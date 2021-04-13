import cv2
import os
import keyboard

files = os.listdir("images")

for i in files:
    path = "images\\" + i

    img = cv2.imread(path)

    cv2.imshow(i,img)   #shows image with its title
    if keyboard.is_pressed("delete"):   #if "delete" is pressed, end program
        break
    cv2.waitKey(0)  #waits until key is pressed to close window
    cv2.destroyAllWindows()