import tkinter as tk
from tkinter import PhotoImage
from screeninfo import get_monitors
from PIL import Image, ImageTk
import random
import os   

class SlideShow:
    def __init__(self, folder_path):
        self.monitor = get_monitors()[-1]
        self.root = tk.Tk()
        self.fullscreen = True
        self.paused = False
        self.root.geometry(f"{self.monitor.width}x{self.monitor.height}+{self.monitor.x}+{self.monitor.y}")
        self.root.attributes('-fullscreen', self.fullscreen)
        
        self.foldePath = folder_path
        self.imageList = getImageList(self.foldePath)
        self.imageLabel = None
        self.loadNewImage()
        
        self.root.bind('<Escape>', lambda event: self.root.quit())
        self.root.bind("<F11>", self.toggleFullscreen)
        self.root.bind("<space>", self.togglePause)
        
        self.root.mainloop()
        
    def toggleFullscreen(self, event):
        self.fullscreen = not(self.fullscreen)
        self.root.attributes('-fullscreen', self.fullscreen)
        
    def togglePause(self, event):
        self.paused = not self.paused
        
    def loadNewImage(self):
        if not self.paused:
            if self.imageLabel:
                self.imageLabel.destroy()
            randomImagePath = getRandomImage(self.imageList, self.foldePath)
            image = Image.open(randomImagePath)
            resizedImage = resize(image, self.monitor)
            photo = ImageTk.PhotoImage(resizedImage)
            self.imageLabel = tk.Label(self.root, image=photo, bg='black')
            self.imageLabel.photo = photo
            self.imageLabel.pack(fill='both', expand=True)
        self.root.after(1000, self.loadNewImage)
        
    
def getImageList(file_path):
    imageList = list()
    for file in os.listdir(file_path):
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
            imageList.append(file)
    return imageList
  
def getRandomImage(imageList, file_path):
    randomImage = random.choice(imageList)
    randomImagePath = os.path.join(file_path, randomImage)
    return randomImagePath

def resize(image: Image, monitor):
    ratio = min((monitor.width / image.width), (monitor.height / image.height))
    newHeight = int(image.height * ratio)
    newWidth = int(image.width * ratio)
    return image.resize((newWidth, newHeight), Image.ANTIALIAS) 

folder_path = 'C:/pathname'
slideShow = SlideShow(folder_path)