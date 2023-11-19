import tkinter as tk
from tkinter import PhotoImage
from screeninfo import get_monitors
from PIL import Image, ImageTk
import os
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2)

NAME_DURATION = 1500
VISIBLE = 255
INVISIBLE = 0
VISIBILITY_TRANSITION = 9
VIS_TRAN_DELAY = 3

class SlideShow:
    def __init__(self, folderPath, imageList, slideDelay):
        #parameters
        self.monitor = get_monitors()[-1]
        self.root = tk.Tk()
        self.isFullscreen = True
        self.isPaused = False
        self.index = -1
        self._after_id = None
        self.slideDelay = slideDelay * 1000
        #root appearance
        self.root.title("Slide Show")
        self.root.geometry(f"{self.monitor.width}x{self.monitor.height}+{self.monitor.x}+{self.monitor.y}")
        self.root.state('zoomed')
        self.root.attributes('-fullscreen', self.isFullscreen)
        #image data
        self.folderPath = folderPath
        self.imageList = imageList
        #canvas
        self.canvas = tk.Canvas(self.root, bg='black', bd=0, highlightthickness=0, relief='ridge')
        self.canvas.pack(fill='both', expand=True)
        self.currentImage = None
        self.currentPhoto = None
        self.currentImageItem = self.initCanvasImage()
        self.nextImage = None
        self.nextPhoto = None
        self.nextImageItem = self.initCanvasImage()
        self.imageNameLabel = None
        #binds
        self.set_binds()
        #start
        startEvent = tk.Event()
        startEvent.keysym = "Right"
        self.bind_loadNewImage(startEvent)
        self.root.mainloop()

    def initCanvasImage(self):
        width = int(self.monitor.width / 2)
        height = int(self.monitor.height / 2)
        imageItem = self.canvas.create_image(width, height, anchor='center', image=None)
        return imageItem
    
    def set_binds(self):
        self.root.bind('<Escape>', self.bind_exit)
        self.root.bind("<F11>", self.bind_toggleFullscreen)
        self.root.bind("<space>", self.bind_togglePause)
        self.root.bind("<Right>", lambda event: self.bind_loadNewImage(event))
        self.root.bind("<Left>", lambda event: self.bind_loadNewImage(event))
        self.root.bind("<Up>", lambda event: self.bind_showImageName(event))
     
    def bind_exit(self, event):
        if self._after_id is not None:
            self._after_id = self.root.after_cancel(self._after_id)
        self.root.destroy()
       
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
        self.root.after(NAME_DURATION, self.imageNameLabel.destroy)
        
    def bind_loadNewImage(self, event):
        if self._after_id is not None:
            self._after_id = self.root.after_cancel(self._after_id)
        if not self.isPaused or event is not None:
            next_index = self.index + 1 if event is None or event.keysym == "Right" else self.index - 1
            self.index = next_index % len(self.imageList)
            self.nextImage = self.getImage()
            if self.currentImage is not None:
                self.fadeImageOutThenIn(VISIBLE, INVISIBLE)
            else:
                self.currentImage = self.nextImage
                self.nextImage = None
                self.fadeInImage(0)
        self._after_id = self.root.after(self.slideDelay, self.bind_loadNewImage, None)
        
    def getImage(self):
        imageName = self.imageList[self.index]
        imagePath = os.path.join(self.folderPath, imageName)
        image = Image.open(imagePath)
        resizedImage = self.resize(image)
        return resizedImage
    
    def resize(self, image: Image):
        ratio = min((self.monitor.width / image.width), (self.monitor.height / image.height))
        newHeight = int(image.height * ratio)
        newWidth = int(image.width * ratio)
        return image.resize((newWidth, newHeight), Image.Resampling.LANCZOS) 
    
    def fadeImageOutThenIn(self, currImgAlpha, nxtImgAlpha):
        #update alpha values
        currImgAlpha_updated = max(INVISIBLE, currImgAlpha - VISIBILITY_TRANSITION)
        nxtImgAlpha_updated = min(VISIBLE, nxtImgAlpha + VISIBILITY_TRANSITION)
        #apply alpha to current image
        self.currentImage.putalpha(currImgAlpha_updated)
        self.currentPhoto = ImageTk.PhotoImage(self.currentImage)
        #apply alpha to next image
        self.nextImage.putalpha(nxtImgAlpha_updated)
        self.nextPhoto = ImageTk.PhotoImage(self.nextImage)
        #adjust images
        self.canvas.itemconfig(self.currentImageItem, image=self.currentPhoto)
        self.canvas.itemconfig(self.nextImageItem, image=self.nextPhoto)
        if currImgAlpha_updated > INVISIBLE and nxtImgAlpha_updated < VISIBLE:
            self.root.after(VIS_TRAN_DELAY, self.fadeImageOutThenIn, currImgAlpha_updated, nxtImgAlpha_updated)
        else:
            self.currentPhoto = self.nextPhoto
            self.currentImage = self.nextImage
            self.canvas.itemconfig(self.currentImageItem, image=self.currentPhoto)
            self.canvas.delete(self.nextImageItem)
            self.nextImageItem = self.initCanvasImage()
            self.nextPhoto = None
    
    def fadeInImage(self, alpha):
        self.currentImage.putalpha(alpha)
        self.currentPhoto = ImageTk.PhotoImage(self.currentImage)
        self.canvas.itemconfig(self.currentImageItem, image=self.currentPhoto)
        if alpha < VISIBLE:
            self.root.after(VIS_TRAN_DELAY, self.fadeInImage, min(VISIBLE, alpha + VISIBILITY_TRANSITION))