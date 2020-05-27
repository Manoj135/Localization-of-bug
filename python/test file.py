import os
with open("C:/Users/Lenovo/Desktop/JSON/commi.txt", 'rb+') as filehandle:
        filehandle.seek(-1, os.SEEK_END)
        filehandle.truncate()
        filehandle.close()
