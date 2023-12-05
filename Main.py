import inputWin as inptWin
import inputState as inptState
import slideshowWin as ss
import random
import os

def getImageList(folderPath, sortBy, startsOrContains_mode, startsOrContains_text):
    imageList = list()
    for file in os.listdir(folderPath):
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".jpe"):
            if startsOrContains_mode == inptState.STARTS and file.startswith(startsOrContains_text):
                imageList.append(file)
            elif startsOrContains_mode == inptState.CONTAINS and startsOrContains_text in file:
                imageList.append(file)
    if sortBy == inptState.NAME:
        imageList.sort()
    if sortBy == inptState.RANDOM:
        imageList = random.sample(imageList, len(imageList))
    return imageList

def main():
    inputState = inptState.InputState()
    while not inputState.didQuit:
        inputWindow = inptWin.InputWindow(inputState)
        inputState.setValues(inputWindow.inputState)
        if inputState.folderPathInput:
            imageList = getImageList(inputState.folderPathInput, inputState.sortBy, inputState.startsOrContains_mode, inputState.startsOrContains_text)
            if len(imageList) == 0:
                print("no images found")
            else:
                slideShow = ss.SlideShow(inputState.folderPathInput, imageList, inputState.fit_mode, inputState.slideDelay)
        else:
            print("no path given")

if __name__ == "__main__":
    main()