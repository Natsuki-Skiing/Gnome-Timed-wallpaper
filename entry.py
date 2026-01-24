class entry:
    def __init__(self,fileLocation:str,time:tuple):
        self.fileLoc = fileLocation
        self.time = time 
    def getMinutes(self)->int:
        hour_str, minute_str, ampm = self.time
        
        h = int(hour_str)
        m = int(minute_str)
        
        
        if ampm == "PM" and h != 12:
            h += 12
        elif ampm == "AM" and h == 12:
            h = 0
            
        return (h * 60) + m