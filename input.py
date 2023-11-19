import tkinter as tk
from tkinter import ttk
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2)

STARTS = 0
CONTAINS = 1
StartsOrContains_Map = {"Starts With:": STARTS, 'Contains:':CONTAINS}

NAME = 0
RANDOM = 1
SortBy_Map = {"Name": NAME, "Random": RANDOM}

ORIGINAL = 0
FIT = 1
FILL = 2
STRETCH = 3
Fit_Map = {"Original": ORIGINAL, "Fit": FIT, "Fill": FILL, "Stretch": STRETCH}

DEFAULT_SLIDE_DELAY = 30

class InputWindow:
    def __init__(self):
        self.folderPathInput = None
        self.startsOrContains_mode = None
        self.startsOrContains = None
        self.sortBy = None
        self.fit_mode = None
        self.slideDelay = None
        self.didQuit = False
        self.row = 0
        
        self.master = tk.Tk()
        self.master.title("Slide Show")
        self.master.protocol("WM_DELETE_WINDOW", self.myQuit)
        
        self.gridConfigure()
        
        self.folderPathInput_Lable = tk.Label(self.master, text="Folder Path:")
        self.folderPathInput_Lable.grid(row=self.row, column=0, sticky="W", padx=5, pady=5)
        self.folderPathInput_Text = tk.Text(self.master, height = 1, spacing1=5, spacing3=5)
        self.folderPathInput_Text.grid(row=self.row, column=1, sticky="W", padx=5, pady=5)
        self.row += 1
        
        self.startsOrContains_Combobox = self.makeComboBox(list(StartsOrContains_Map.keys()), STARTS)
        self.startsOrContains_Combobox.grid(row=self.row, column=0, sticky="W", padx=5, pady=5)
        self.startsOrContains_Text = tk.Text(self.master, height = 1, spacing1=5, spacing3=5)
        self.startsOrContains_Text.grid(row=self.row, column=1, sticky="W", padx=5, pady=5)
        self.row += 1
        
        self.sortBy_Label = tk.Label(self.master, text="Sort By:")
        self.sortBy_Label.grid(row=self.row, column=0, sticky="W", padx=5, pady=5)
        self.sortBy_Combobox = self.makeComboBox(list(SortBy_Map.keys()), RANDOM)
        self.sortBy_Combobox.grid(row=self.row, column=1, sticky="W", padx=5, pady=5)
        self.row += 1
        
        self.fit_Label = tk.Label(self.master, text="Fit:")
        self.fit_Label.grid(row=self.row, column=0, sticky="W", padx=5, pady=5)
        self.fit_Combobox = self.makeComboBox(list(Fit_Map.keys()), FIT)
        self.fit_Combobox.grid(row=self.row, column=1, sticky="W", padx=5, pady=5)
        self.row += 1
        
        self.slideDelay_Selection = tk.IntVar(master=self.master, value=DEFAULT_SLIDE_DELAY)
        self.slideDelay_Label_1 = tk.Label(self.master, text="Speed In Seconds:")
        self.slideDelay_Label_1.grid(row=self.row, column=0, sticky="W", padx=5, pady=5)
        #self.slideDelay_Label_2 = tk.Label(self.master, text=str(self.slideDelay_Selection.get()) + " Seconds")
        #self.slideDelay_Label_2.grid(row=self.row, column=1, sticky="W", padx=5, pady=5)
        self.slideDelay_Slider = tk.Scale(self.master, from_=1, to=180, orient='horizontal', command=self.sliderChanged, variable=self.slideDelay_Selection, length=360)
        self.slideDelay_Slider.grid(row=self.row, column=1, padx=5, pady=5)
        self.row += 1
        
        self.start_Button = tk.Button(self.master, text = "Start", command = self.getInputAndClose)
        self.start_Button.grid(row=self.row, column=0, padx=5, pady=5)
        self.quit_Button = tk.Button(self.master, text = "Quit", command = self.myQuit)
        self.quit_Button.grid(row=self.row, column=1, padx=5, pady=5)
        self.row += 1

        self.master.mainloop()
    
    def gridConfigure(self):
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
      
    def makeComboBox(self, values, defaultValueIndex):
        combobox = ttk.Combobox(state="readonly", values=values)
        combobox.set(value=values[defaultValueIndex])
        return combobox
        
    def getRowAndAdvance(self, toAdvance):
        row = self.row
        if toAdvance:
            self.row += 1
        return row
        
    def makeRadioButtons(self):
        radioButtons = list()
        col = 1
        buttonValues = {"Name": NAME, "Random": RANDOM}
        for (text, value) in buttonValues.items():
            radioButton =  tk.Radiobutton(self.master,
                                          text = text,
                                          value = value,
                                          variable = self.sortBy_selection)
            radioButton.grid(row=self.getRowAndAdvance(False), column=col, sticky="W", padx=5, pady=5)
            col += 1
            radioButtons.append(radioButton)
        self.row += 1
        return radioButtons
        
    def sliderChanged(self, event):
        self.slideDelay_Label_2.configure(text=str(self.slideDelay_Selection.get()) + " Seconds")
        
    def getInputAndClose(self):
        self.folderPathInput = self.folderPathInput_Text.get(1.0, "end-1c").replace('\\','/')
        self.startsOrContains_mode = StartsOrContains_Map[self.startsOrContains_Combobox.get()]
        self.startsOrContains = self.startsOrContains_Text.get(1.0, "end-1c")
        self.sortBy = SortBy_Map[self.sortBy_Combobox.get()]
        self.fit_mode = Fit_Map[self.fit_Combobox.get()]
        self.slideDelay = self.slideDelay_Selection.get()
        self.master.destroy()
        
    def myQuit(self):
        self.didQuit = True
        self.master.quit()