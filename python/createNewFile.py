import re
import os
import glob
from os import path

def listToString(s):   
    str1 = " "     
    return (str1.join(s))
fields = ["build_name", "package_name", "pakage_link", "file_name", "file_link", "commit_id", "tokens"]
ist = []
num = 1
base_path = "C:/Users/Lenovo/Desktop/JSON/py1/tokens0.txt"
with open (base_path) as in_file:
        for line in in_file:
            ist.append(line.strip())
        print(len(ist))
        print(os.stat(base_path).st_size)
        in_file = open(base_path,"w")
        in_file.write("{\n\"fields\" : {\n")
        for i in range(len(fields)):
            if(i==len(fields)-1):
                st = listToString(ist[i:])
                in_file.write("\t\t\""+fields[i]+"\": [\""+st+"\"]\n},\n")
            else:
                in_file.write("\t\t\""+fields[i]+"\": \""+ist[i]+"\",\n")
        in_file.write("\"id\" : \""+str(num)+"\",\n\"type\" : \"add\"\n}")
        num = num+1
        in_file.close()

            
