import tkinter as tk
from tkinter import PhotoImage
from screeninfo import get_monitors
from PIL import Image, ImageTk
import random
import os   

def show_image(file_path):
    monitors = get_monitors()
    monitor = monitors[-1]
    
    root=tk.Tk()
    root.geometry(f"{monitor.width}x{monitor.height}+{monitor.x}+{monitor.y}")
    root.attributes('-fullscreen', True)
    
    root.bind('<Escape>', lambda event: root.quit())
    root.bind("<F11>", lambda event: toggleFullscreen(root))
    
    imageList = getImageList(file_path)
    image_path = getRandomImage(imageList, file_path)
    image = Image.open(image_path)
    resizedImage = resize(image, monitor)
    photo = ImageTk.PhotoImage(resizedImage)

    label = tk.Label(root, image=photo, bg='black')
    label.photo = photo
    label.pack(fill='both', expand=True)
    
    root.mainloop()
    
    
def getImageList(file_path):
    ImageList = list()
    for file in os.listdir(file_path):
        if file.endswith(".png") or file.endswith(".jpg") or file.endswith(".jpeg"):
            ImageList.append(file)
    return ImageList
  
def getRandomImage(imageList, file_path):
    randomImage = random.choice(imageList)
    randomImagePath = os.path.join(file_path, randomImage)
    return randomImagePath

def resize(image: Image, monitor):
    ratio = min((monitor.width / image.width), (monitor.height / image.height))
    newHeight = int(image.height * ratio)
    newWidth = int(image.width * ratio)
    return image.resize((newWidth, newHeight), Image.ANTIALIAS) 

def toggleFullscreen(root):
    fullscreen = root.attributes('-fullscreen')
    fullscreen = not(fullscreen)
    root.attributes('-fullscreen', fullscreen)

file_path = 'C:/pathname'
show_image(file_path)