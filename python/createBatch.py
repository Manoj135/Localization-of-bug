import re
import glob
import os
from os import path

def listToString(s):   
    str1 = " "     
    return (str1.join(s))
fields = ["build_name", "package_name", "pakage_link", "file_name", "file_link", "commit_id", "commit_date", "tokens"]
ist = []
num = 1
batch = 1
base_path = "C:/Users/Lenovo/Desktop/JSON/py1/*.txt"
batch_path = "C:/Users/Lenovo/Desktop/JSON/py/batch"
files = glob.glob(base_path) 
for file in files:
    print(file)
    with open (file) as in_file:
            for line in in_file:
                ist.append(line.strip())
            in_file.close()
    print(len(ist))
    with open(batch_path+str(batch)+".txt","a+") as out_file:
                if(os.stat(file).st_size+os.stat(batch_path+str(batch)+".txt").st_size>5237760):
                    with open(batch_path+str(batch)+".txt", 'rb+') as filehandle:
                            filehandle.seek(-1, os.SEEK_END)
                            filehandle.truncate()
                            filehandle.truncate()
                            filehandle.close()
                    out_file.write("\n]")
                    batch = batch+1
                    out_file = open(batch_path+str(batch)+".txt","a+")
                if(os.stat(batch_path+str(batch)+".txt").st_size==0):
                    out_file.write("[\n")
                out_file.write("{\n\"fields\" : {\n")
                for i in range(len(fields)):
                    if(i==len(fields)-1):
                        st = listToString(ist[i:])
                        out_file.write("\t\t\""+fields[i]+"\": [\""+st+"\"]\n},\n")
                    else:
                        out_file.write("\t\t\""+fields[i]+"\": \""+ist[i]+"\",\n")
                out_file.write("\"id\" : \""+str(num)+"\",\n\"type\" : \"add\"\n},\n")
                ist = []
                num = num+1
                out_file.close()
with open(batch_path+str(batch)+".txt", 'rb+') as filehandle:
        filehandle.seek(-1, os.SEEK_END)
        filehandle.truncate()
        filehandle.truncate()
        filehandle.close()
