import tkinter as tk
from tkinter import PhotoImage
from screeninfo import get_monitors
from PIL import Image, ImageTk
import input
import random
import os
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2)

class SlideShow:
    def __init__(self, folder_path):
        #parameters
        self.monitor = get_monitors()[-1]
        self.root = tk.Tk()
        self.isFullscreen = True
        self.isPaused = False
        self.index = -1
        self._after_id = None
        self.slideDelay = 22000
        self.nameDisplayDuration = 1500
        #root appearance
        self.root.geometry(f"{self.monitor.width}x{self.monitor.height}+{self.monitor.x}+{self.monitor.y}")
        self.root.state('zoomed')
        self.root.attributes('-fullscreen', self.isFullscreen)
        #image
        self.foldePath = folder_path
        self.imageList = getImageList(self.foldePath)
        self.imageLabel = tk.Label(self.root, bg='black')
        self.imageLabel.pack(fill='both', expand=True)
        self.image = None
        self.imageNameLabel = None
        #binds
        self.set_binds()
        #start
        startEvent = tk.Event()
        startEvent.keysym = "Right"
        self.bind_loadNewImage(startEvent)
        self.root.mainloop()
    
    def set_binds(self):
        self.root.bind('<Escape>', lambda event: self.root.quit())
        self.root.bind("<F11>", self.bind_toggleFullscreen)
        self.root.bind("<space>", self.bind_togglePause)
        self.root.bind("<Right>", lambda event: self.bind_loadNewImage(event))
        self.root.bind("<Left>", lambda event: self.bind_loadNewImage(event))
        self.root.bind("<Up>", lambda event: self.bind_showImageName(event))
        
    def bind_toggleFullscreen(self, event):
        self.isFullscreen = not(self.isFullscreen)
        self.root.attributes('-fullscreen', self.isFullscreen)
        
    def bind_togglePause(self, event):
        self.isPaused = not self.isPaused
        
    def bind_showImageName(self, event):
        if self.imageNameLabel:
            self.imageNameLabel.destroy()
        image_name = self.imageList[self.index]
        self.imageNameLabel = tk.Label(
            self.root,
            text=image_name,
            font=("Helvetica bold", 18),
            fg="light gray",
            bg="black",
        )
        self.imageNameLabel.place(
            relx=0.5, rely=0.978, anchor="s"
        )
        self.root.after(self.nameDisplayDuration, self.imageNameLabel.destroy)
        
    def bind_loadNewImage(self, event):
        if self._after_id is not None:
            self.root.after_cancel(self._after_id)
        if not self.isPaused or event is not None:
            next_index = self.index + 1 if event is None or event.keysym == "Right" else self.index - 1
            self.index = next_index % len(self.imageList)
            nextImage = self.getImage()
            if self.image is not None:
                self.fadeImageOutThenIn(255, nextImage)
            else:
                self.image = nextImage
                self.fadeInImage(0)
        self._after_id = self.root.after(self.slideDelay, self.bind_loadNewImage, None)
        
    def getImage(self):
        imageName = self.imageList[self.index]
        imagePath = os.path.join(self.foldePath, imageName)
        image = Image.open(imagePath)
        resizedImage = resize(image, self.monitor)
        return resizedImage     
    
    def fadeImageOutThenIn(self, alpha, nextImage):
        self.image.putalpha(alpha)
        photo = ImageTk.PhotoImage(self.image)
        self.imageLabel.configure(image=photo)
        self.imageLabel.photo = photo
        if alpha > 1:
            self.root.after(2, self.fadeImageOutThenIn, max(0, alpha - 24), nextImage)
        else:
            self.image = nextImage
            self.fadeInImage(0)
    
    def fadeInImage(self, alpha):
        self.image.putalpha(alpha)
        photo = ImageTk.PhotoImage(self.image)
        self.imageLabel.configure(image=photo)
        self.imageLabel.photo = photo
        if alpha < 254:
            self.root.after(10, self.fadeInImage, min(255, alpha + 8))
    
def getImageList(file_path):
    imageList = list()
    for file in os.listdir(file_path):
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
            imageList.append(file)
    imageList = random.sample(imageList, len(imageList))
    return imageList

def resize(image: Image, monitor):
    ratio = min((monitor.width / image.width), (monitor.height / image.height))
    newHeight = int(image.height * ratio)
    newWidth = int(image.width * ratio)
    return image.resize((newWidth, newHeight), Image.Resampling.LANCZOS) 

def main():
    inputWindow = input.InputWindow()
    folder_path = inputWindow.input
    slideShow = SlideShow(folder_path)

if __name__ == "__main__":
    main()