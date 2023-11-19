import input
import slideshow as ss
import random
import os

def getImageList(folderPath, sortBy, startsOrContains_mode, startsOrContains_text):
    imageList = list()
    for file in os.listdir(folderPath):
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg") or file.endswith(".jpe"):
            if startsOrContains_mode == input.STARTS and file.startswith(startsOrContains_text):
                imageList.append(file)
            elif startsOrContains_mode == input.CONTAINS and startsOrContains_text in file:
                imageList.append(file)
    if sortBy == input.NAME:
        imageList.sort()
    if sortBy == input.RANDOM:
        imageList = random.sample(imageList, len(imageList))
    return imageList

def main():
    folderPath = ''
    didQuit = False
    while not folderPath and not didQuit:
        inputWindow = input.InputWindow()
        folderPath = inputWindow.folderPathInput
        startsOrContains_mode = inputWindow.startsOrContains_mode
        startsOrContains_text = inputWindow.startsOrContains
        sortBy = inputWindow.sortBy
        fit = inputWindow.fit_mode #TODO
        slideDelay = inputWindow.slideDelay
        didQuit = inputWindow.didQuit
        
        imageList = getImageList(folderPath, sortBy, startsOrContains_mode, startsOrContains_text)
        if len(imageList) == 0:
            print("error")
        elif not folderPath:
            print("error")
        else:
            slideShow = ss.SlideShow(folderPath, imageList, slideDelay)
        folderPath = ''

if __name__ == "__main__":
    main()