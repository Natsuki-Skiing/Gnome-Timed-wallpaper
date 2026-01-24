import time 
from entry import *
import json
import os
import datetime
import subprocess
from pathlib import Path
class timedWallpaperBackground:
    def __init__(self):
        with open("config.json","r") as file:
            data = json.loads(file.read())
        self.delay = data["secondsBetweenChecks"]
        self.currentSet = None
        self.mainLoop()
    def mainLoop(self):
        while(True):
            with open("config.json","r") as file:
                self.currentSet = json.loads(file.read())["currentSet"]
            self.setWallpaper()
            time.sleep(self.delay)
    def setWallpaper(self):
        if(self.currentSet):
            entries = []
            try:
               with open(self.currentSet, "r") as file:
                data = json.loads(file.read())
                self.entryDict = dict()
                
                for item in data:
                    
                    new_entry = entry(item["fileLoc"], item["time"])
                    entries.append(new_entry)
                    
                
                entries.sort(key=lambda x: x.getMinutes())

               
                now = datetime.datetime.now()
                current_minutes = (now.hour * 60) + now.minute

                found_wallpaper = False

                
                for index in range(len(entries) - 1, -1, -1):
                    if current_minutes >= entries[index].getMinutes():
                        self.changeWallpaper(entries[index].fileLoc)
                        found_wallpaper = True
                        break

                
                if not found_wallpaper and len(entries) > 0:
                    self.changeWallpaper(entries[-1].fileLoc)
            except:
                pass
    def changeWallpaper(self,path:str):
        abs_path = os.path.abspath(path)
        uri = f"file://{abs_path}"

       
        subprocess.run([
            "gsettings", "set",
            "org.gnome.desktop.background",
            "picture-uri-dark",
            uri
        ])

        subprocess.run([
            "gsettings", "set",
            "org.gnome.desktop.background",
            "picture-uri",
            uri
        ])



if __name__ == "__main__":
    process = timedWallpaperBackground()
    