import inputState as inptState
import tkinter as tk
from tkinter import ttk
import ctypes
ctypes.windll.shcore.SetProcessDpiAwareness(2)

class InputWindow:
    def __init__(self, inputState: inptState.InputState):
        self.inputState = inputState
        self.row = 0
        
        self.master = tk.Tk()
        self.master.title("Slide Show")
        self.master.protocol("WM_DELETE_WINDOW", self.myQuit)
        
        self.gridConfigure()
        
        self.folderPathInput_Lable = tk.Label(self.master, text="Folder Path:")
        self.folderPathInput_Lable.grid(row=self.row, column=0, sticky="W", padx=5, pady=5)
        self.folderPathInput_Text = tk.Text(self.master, height = 1, spacing1=5, spacing3=5, xscrollcommand=set(), width=55)
        self.folderPathInput_Text.insert(0.0, self.inputState.folderPathInput)
        self.folderPathInput_Text.grid(row=self.row, column=1, sticky="W", padx=5, pady=5)
        self.row += 1
        
        self.startsOrContains_Combobox = self.makeComboBox(list(inptState.StartsOrContains_Map.keys()), self.inputState.startsOrContains_mode)
        self.startsOrContains_Combobox.grid(row=self.row, column=0, sticky="W", padx=5, pady=5)
        self.startsOrContains_Text = tk.Text(self.master, height = 1, spacing1=5, spacing3=5, xscrollcommand=set(), width=55)
        self.startsOrContains_Text.insert(0.0, self.inputState.startsOrContains_text)
        self.startsOrContains_Text.grid(row=self.row, column=1, sticky="W", padx=5, pady=5)
        self.row += 1
        
        self.sortBy_Label = tk.Label(self.master, text="Sort By:")
        self.sortBy_Label.grid(row=self.row, column=0, sticky="W", padx=5, pady=5)
        self.sortBy_Combobox = self.makeComboBox(list(inptState.SortBy_Map.keys()), self.inputState.sortBy)
        self.sortBy_Combobox.grid(row=self.row, column=1, sticky="W", padx=5, pady=5)
        self.row += 1
        
        self.fit_Label = tk.Label(self.master, text="Fit:")
        self.fit_Label.grid(row=self.row, column=0, sticky="W", padx=5, pady=5)
        self.fit_Combobox = self.makeComboBox(list(inptState.Fit_Map.keys()), self.inputState.fit_mode)
        self.fit_Combobox.grid(row=self.row, column=1, sticky="W", padx=5, pady=5)
        self.row += 1
        
        self.slideDelay_Selection = tk.IntVar(master=self.master, value=self.inputState.slideDelay)
        self.slideDelay_Label = tk.Label(self.master, text="Speed In Seconds:")
        self.slideDelay_Label.grid(row=self.row, column=0, sticky="W", padx=5, pady=5)
        self.slideDelay_Slider = tk.Scale(self.master, from_=1, to=180, orient='horizontal', variable=self.slideDelay_Selection, length=360)
        self.slideDelay_Slider.grid(row=self.row, column=1, padx=5, pady=5)
        self.row += 1
        
        self.start_Button = tk.Button(self.master, text = "Start", command = self.getInputAndClose, relief="raised", overrelief="solid", width=8, borderwidth=3)
        self.start_Button.grid(row=self.row, column=0, padx=5, pady=5)
        self.quit_Button = tk.Button(self.master, text = "Quit", command = self.myQuit, relief="raised", overrelief="solid", width=8, borderwidth=3)
        self.quit_Button.grid(row=self.row, column=1, padx=5, pady=5)
        self.row += 1

        self.master.mainloop()
    
    def gridConfigure(self):
        self.master.columnconfigure(0, weight=1)
        self.master.columnconfigure(1, weight=1)
      
    def makeComboBox(self, values, defaultValueIndex):
        combobox = ttk.Combobox(state="readonly", values=values, width=12)
        combobox.set(value=values[defaultValueIndex])
        return combobox
        
    def getInputAndClose(self):
        self.inputState.folderPathInput = self.folderPathInput_Text.get(1.0, "end-1c").replace('\\','/')
        self.inputState.startsOrContains_mode = inptState.StartsOrContains_Map[self.startsOrContains_Combobox.get()]
        self.inputState.startsOrContains_text = self.startsOrContains_Text.get(1.0, "end-1c")
        self.inputState.sortBy = inptState.SortBy_Map[self.sortBy_Combobox.get()]
        self.inputState.fit_mode = inptState.Fit_Map[self.fit_Combobox.get()]
        self.inputState.slideDelay = self.slideDelay_Selection.get()
        self.master.destroy()
        
    def myQuit(self):
        self.inputState.didQuit = True
        self.master.quit()