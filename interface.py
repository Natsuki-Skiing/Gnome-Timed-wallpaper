
import tkinter as tk
import json
import os
import time
from tkinter import ttk ,messagebox ,filedialog ,PhotoImage
from PIL import Image, ImageTk
from entry import *
import tkinter.simpledialog 

class SetManager(tk.Toplevel):
    def __init__(self, parent=None, callback=None):
        super().__init__(parent)
        self.callback = callback
        self.title("Manage Wallpaper Sets")
        self.geometry("400x300")
        
        
        self.sets_dir = "sets"
        if not os.path.exists(self.sets_dir):
            os.makedirs(self.sets_dir)

        self._createWidgets()
        self._layoutWidgets()
        self._populateList()
    
    def _createWidgets(self):
        
        self.list_frame = ttk.Frame(self)
        self.scrollbar = ttk.Scrollbar(self.list_frame, orient="vertical")
        self.lbSets = tk.Listbox(self.list_frame, yscrollcommand=self.scrollbar.set, font=("Arial", 11))
        self.scrollbar.config(command=self.lbSets.yview)

        
        self.btn_frame = ttk.Frame(self)
        self.btnNew = ttk.Button(self.btn_frame, text="New Set", command=self.create_new_set)
        self.btnDelete = ttk.Button(self.btn_frame, text="Delete Set", command=self.delete_set)
        self.btnSetActive = ttk.Button(self.btn_frame, text="Set Active", command=self.set_active)

    def _layoutWidgets(self):
        
        self.grid_columnconfigure(0, weight=1) 
        self.grid_columnconfigure(1, weight=0) 
        self.grid_rowconfigure(0, weight=1)

        
        self.list_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.lbSets.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

       
        self.btn_frame.grid(row=0, column=1, sticky="n", padx=10, pady=10)
        self.btnNew.pack(fill="x", pady=5)
        self.btnDelete.pack(fill="x", pady=5)
        
        
        ttk.Separator(self.btn_frame, orient='horizontal').pack(fill='x', pady=10)
        
        self.btnSetActive.pack(fill="x", pady=5)

    def _populateList(self):
        self.lbSets.delete(0, tk.END)
        try:
            files = os.listdir(self.sets_dir)
            for f in files:
                if f.endswith(".json"):
                   
                    name = os.path.splitext(f)[0]
                    self.lbSets.insert(tk.END, name)
        except OSError as e:
            tk.messagebox.showerror("Error", f"Could not read sets directory: {e}")
    
    def create_new_set(self):
        
        new_name = tk.simpledialog.askstring("New Set", "Enter name for new set:", parent=self)
        
        if new_name:
           
            if not new_name.isalnum():
                tk.messagebox.showwarning("Invalid Name", "Please use alphanumeric characters only.")
                return

            file_path = os.path.join(self.sets_dir, f"{new_name}.json")
            
            if os.path.exists(file_path):
                tk.messagebox.showerror("Error", "A set with this name already exists.")
                return

            # Create empty JSON file (empty list)
            try:
                with open(file_path, "w") as f:
                    json.dump([], f)
                self._populateList()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to create file: {e}")

    def delete_set(self):
        selection = self.lbSets.curselection()
        if not selection:
            return

        set_name = self.lbSets.get(selection[0])
        file_path = os.path.join(self.sets_dir, f"{set_name}.json")

        confirm = tk.messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{set_name}'?")
        if confirm:
            try:
                os.remove(file_path)
                self._populateList()
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to delete file: {e}")

    def set_active(self):
        selection = self.lbSets.curselection()
        if not selection:
            tk.messagebox.showwarning("Selection Required", "Please select a set from the list.")
            return

        set_name = self.lbSets.get(selection[0])
       
        full_path = os.path.join(self.sets_dir, f"{set_name}.json")

        if self.callback:
            self.callback(full_path)
            self.destroy()

        import backGroundProcess

        backProcess = backGroundProcess()
        backProcess.setWallpaper()
        backProcess.destroy()



class TimeSelector(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding="10 10 10 10")
        self.pack()

       
        self.hour_var = tk.StringVar(value="10")
        self.minute_var = tk.StringVar(value="30")
        self.ampm_var = tk.StringVar(value="AM")

        ttk.Label(self, text="Hour:").grid(row=0, column=0)
        self.hour_spinbox = ttk.Spinbox(
            self,
            from_=1, to=12,
            wrap=True,
            width=5,
            textvariable=self.hour_var
        )
        self.hour_spinbox.grid(row=0, column=1)

       
        ttk.Label(self, text=":").grid(row=0, column=2)

        
        ttk.Label(self, text="Minute:").grid(row=0, column=3)
        self.minute_spinbox = ttk.Spinbox(
            self,
            from_=0, to=59,
            wrap=True,
            width=5,
            increment=5,
            textvariable=self.minute_var
        )
        self.minute_spinbox.grid(row=0, column=4)
        
        
        self.ampm_combo = ttk.Combobox(
            self,
            textvariable=self.ampm_var,
            values=["AM", "PM"],
            width=4,
            state="readonly"
        )
        self.ampm_combo.grid(row=0, column=5, padx=5)


    def get_time(self):
        hour = self.hour_var.get()
        minute = self.minute_var.get()
        ampm = self.ampm_var.get()
        return(hour,minute,ampm)
    
    def set_time(self, time_tuple):
        """
        Sets the time displayed by the widgets using a tuple.

        :param time_tuple: A tuple in the format (hour_str, minute_str, ampm_str)
                           e.g., ("10", "30", "PM")
        """
        
        try:
            hour_str, minute_str, ampm_str = time_tuple
        except ValueError:
            print("Error: Input must be a tuple with three elements (hour, minute, ampm).")
            return

        
        if hour_str.isdigit() and 1 <= int(hour_str) <= 12:
            self.hour_var.set(hour_str.zfill(2)) 
        else:
            print(f"Warning: Invalid hour value '{hour_str}'. Not set.")

       
        if minute_str.isdigit() and 0 <= int(minute_str) <= 59:
            self.minute_var.set(minute_str.zfill(2)) #  zfill to ensure two digits
        else:
            print(f"Warning: Invalid minute value '{minute_str}'. Not set.")

        
        ampm_upper = ampm_str.upper()
        if ampm_upper in ("AM", "PM"):
            self.ampm_var.set(ampm_upper)
        else:
            print(f"Warning: Invalid AM/PM value '{ampm_str}'. Not set.")
class editMenu(tk.Toplevel):
    def __init__(self,parent=None, entry=None, callback=None):
        super().__init__(parent)
        self.callback = callback
        self._createWidgets()
        self._placeWidgets()
        if entry:
            self.title("Edit Menu")
            self.entFileName.insert(0,entry.fileLoc)
            self.timeSelector.set_time(entry.time)
            
        else:
            self.title("New Menu")
        self.geometry("630x400")
        
        

    def _createWidgets(self):
        self.lbFileName = ttk.Label(self,text="File Location")
        self.entFileName = ttk.Entry(self,width=150)
        self.btnFileFile = ttk.Button(self,text="Find Image",command =self.findImage)
        self.timeFrame = ttk.Frame(self)
        self.timeSelector = TimeSelector(self.timeFrame)
        self.btnAdd = ttk.Button(self,text="Add to set",command= self.done)
    def findImage(self):
        dir = self.getFileName()
        self.entFileName.delete(0)
        self.entFileName.insert(0,dir)
    def getFileName(self)->str:
        return(tk.filedialog.askopenfilename(title="Select Picture",initialdir = os.path.expanduser("~/Pictures"),filetypes=[
        ('Image files', '*.jpg *.png *.jpeg'),
        ('All files', '*.*')
    ]))
    def done(self):
        dir = self.entFileName.get()
        if(dir == ""):
            tk.messagebox.showerror("Empty file","You must select an image to add. Use 'Find Image' button or type the path")
        elif(not os.path.exists(dir)):
            tk.messagebox.showerror("Path Error","Unable to locate image from given path, does it exist ?")
        else:
            timeTup = self.timeSelector.get_time()
            newEntry = entry(dir,timeTup)
            if self.callback:
                self.callback(newEntry)
            self.destroy()
    def _placeWidgets(self):
        self.grid_columnconfigure(0, weight=0)
       
        self.grid_columnconfigure(1, weight=5) 
       
        self.grid_columnconfigure(2, weight=0)
        
       
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_rowconfigure(2, weight=1)

       
        self.lbFileName.grid(row=0, column=0, padx=(10, 5), pady=10, sticky="w")
        self.entFileName.grid(row=0, column=1, padx=5, pady=10, sticky="ew")
        self.btnFileFile.grid(row=0, column=2, padx=(5, 10), pady=10, sticky="e")

        
        self.timeFrame.grid(row=1, column=1, padx=5, pady=10, sticky="w")

        
        self.btnAdd.grid(row=2, column=0, columnspan=3, padx=10, pady=10, sticky="se")
class interface(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.geometry("1000x600")
        self.configDict = self.loadConfig()
        self.counter_value = 0
        self.entryDict = dict()
        self._createWidgets()
        self._layoutWidgets()
        self.config = self.loadConfig()
        self.currentPrevImage = None
        self.selectedItem = None
        if(not self.checkSetValidity()):
            tk.messagebox.showerror(title="No Active Set", message="You Must create a set and select an active set. Taking you to the set menu" )
            self.setMenu()
        self.setTitle()
        self.loadSet()
    def loadSet(self):
        try:
            with open(self.configDict["currentSet"],"r") as file:
                data = json.loads(file.read())
                self.entryDict = dict()
                for item in data:
                    name = os.path.basename(item["fileLoc"])
                    timeStr =f"{item["time"][0]} : {item["time"][1]} {item["time"][2]}"
                    self.entryDict[name] = entry(item["fileLoc"],item["time"])
                    self.table.insert(parent="",index=tk.END,values=(name,timeStr))
                pass 
        except:
            tk.messagebox.showerror("Failed Loading set", "Failed to load entries from current set ")
    def setTitle(self):
        self.title(f"Timed Wallpaper For Linux -- {self.configDict["currentSet"]}")
    def checkSetValidity(self)->bool:
        return(os.path.isfile(self.configDict["currentSet"]))
    def _createMenuBar(self):
        pass
    def loadEntryList(self):
        pass
    def loadConfig(self) ->dict:
        config = None
        try:
            with open("config.json","r") as file:
                config = json.loads(file.read())
        except:
            tk.messagebox.showwarning(title="No Config File", message="No config file was found, creating one with default settings, these can be altered :]", )
            config = {"currentSet":"","secondsBetweenChecks":330}
            with open("config.json","w") as file:
                file.write(json.dumps(config))


        return(config)
    def setMenu(self):
    
        if(not os.path.isdir("sets")):
            os.mkdir("sets")


        managerWin = SetManager(parent=self, callback=self.onSetSelected)
        managerWin.grab_set()
    def onSetSelected(self,filePath):
        self.configDict["currentSet"] = filePath
        self.selectedItem =None 
        self.entryDict = dict()
        # Save to config.json
        with open("config.json", "w") as f:
            json.dump(self.configDict, f)
        self.setTitle()
        self.table.delete(*self.table.get_children())
        self.loadSet()
    def _createWidgets(self):
        """Creates all necessary widgets for the application."""
        
        
        self.table = ttk.Treeview()
        self.table["columns"] = ("fileCol", "timeCol")
        self.table.column("#0", width=0, stretch=tk.NO)
        self.table.column("fileCol",width=100)
        self.table.column("timeCol",width=100)
        
        self.table.heading("fileCol",text="File Name")
        self.table.heading("timeCol",text="Time When Set")
        self.table.bind("<<TreeviewSelect>>", self.onEntryClicked)
        self.btnAdd = ttk.Button(text="Add",command=self.addWallpaper)
        self.btnEdit = ttk.Button(text="Edit",command=self.editWallpaper)
        self.btnRemove = ttk.Button(text="Remove",command=self.removeWallpaper)
        self.btnSets = ttk.Button(text="Set Manager",command=self.setMenu)
        self.imgLable = ttk.Label()
    def onEntryClicked(self,event):
        selectedItem = self.table.selection()

        if selectedItem:
            itemID = selectedItem[0]
            self.itemID = itemID
            self.selectedItem = self.table.item(itemID)
            dictKey = self.table.item(itemID)['values'][0]
            self.loadImagePreviw(self.entryDict[dictKey].fileLoc)
    def writeSet(self):
        try:
            data= [item.__dict__ for item in self.entryDict.values()]
            with open(self.configDict["currentSet"],"w") as file:
                file.write(json.dumps(data))
        except:
            tk.messagebox.showerror(title="Set Writing Failed", message=f"Faild to write changes to {self.configDict["currentSet"]}" )
    def addWallpaper(self):
        if(self.checkSetValidity()):
            addWindow = editMenu(parent=self,callback = self.addEntry)
            addWindow.grab_set() 
            
    def editWallpaper(self):
        if(self.checkSetValidity()):
            if self.selectedItem:
                addWindow = editMenu(parent=self,callback = self.addEntry,entry=self.entryDict[self.selectedItem['values'][0]])
                
                addWindow.grab_set()
                self.removeWallpaper()
                
            else:
                tk.messagebox.showwarning(title="No Selection made", message="You must select and entry from the list, selected items are highlighted" )
            
    def removeWallpaper(self):
        if(self.checkSetValidity()):
            if self.selectedItem:
                
                self.entryDict.pop(self.selectedItem['values'][0])
                self.table.delete(self.itemID)
                self.writeSet()
            else:
                tk.messagebox.showwarning(title="No Selection made", message="You must select and entry from the list, selected items are highlighted" )
    def addEntry(self,newEntry:entry):
        timeString = f"{newEntry.time[0]} : {newEntry.time[1]} {newEntry.time[2]}"
        name = os.path.basename(newEntry.fileLoc)
        self.entryDict[name] = newEntry
        self.table.insert(parent="",index=tk.END,values=(name,timeString))
        self.writeSet()
    def loadImagePreviw(self,filePath:str):
        if(os.path.isfile(filePath)):
            try:
                pillImage = Image.open(filePath) 
                pillImage.thumbnail((550,550),Image.Resampling.LANCZOS)
                self.currentPrevImage = ImageTk.PhotoImage(pillImage)
                self.imgLable.config(image=self.currentPrevImage)
            except:
                tk.messagebox.showwarning(title="Error Loading Image", message="File has been found but failed to load, is the file an image?" )
        else:
            tk.messagebox.showwarning(title="Error Loading Image", message="Cannot Load image, has it been moved , deleted or renamed?" )
    def _layoutWidgets(self):
        
        self.grid_columnconfigure(0, weight=1) 
        
        self.grid_columnconfigure(1, weight=3) #
        self.grid_columnconfigure(2, weight=3) 
       
        self.grid_columnconfigure(3, weight=0) 

    
        self.grid_rowconfigure(0, weight=1) 
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1) #

       
        self.imgLable.grid(
            row=0,
            column=0,
            rowspan=3,      
            padx=10, 
            pady=10, 
            sticky="nsew"   
        )
        
      
        self.table.grid(
            row=0,          
            column=1,       
            columnspan=2,   
            rowspan=3,      
            padx=(5, 5),    
            pady=10,
            sticky="nsew"
        )

        
        
       
        self.btnAdd.grid(
            row=0, 
            column=3, 
            padx=(5, 10), 
            pady=10, 
            sticky="ew"
        )

       
        self.btnEdit.grid(
            row=1, 
            column=3, 
            padx=(5, 10), 
            pady=10, 
            sticky="ew"
        )
        
        
        self.btnRemove.grid(
            row=2, 
            column=3, 
            padx=(5, 10), 
            pady=10, 
            sticky="ew"
        )
        self.btnSets.grid(
            row=3, 
            column=3, 
            padx=(5, 10), 
            pady=10, 
            sticky="ew"
        )
    
if __name__ == "__main__":
    test = interface()
    
    test.mainloop()
    

    

    pass