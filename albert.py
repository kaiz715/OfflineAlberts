import cv2
import pytesseract 
import os



pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
def analyze():
    
    numFiles = len(os.listdir("images"))
    for i in range(0,numFiles):
        path = "images\\" + str(i) + ".png"    #path of image
        
        img = cv2.imread(path)      #loads image from path
        text = pytesseract.image_to_string(img)     #returns all text found

        x = text.find(")")      #in the text, find the first closed )
        title = text[:x+1]      #truncate to title
        title = title.replace(":","").replace("?","").replace("\n","").replace("/","").strip()

        newPath = "images\\" + title + ".png"

        try: 
            os.rename(path, newPath)    #tries to rename file
        except Exception as e:  #if doesn't work, print error and pass
            print(e)
            pass

analyze()