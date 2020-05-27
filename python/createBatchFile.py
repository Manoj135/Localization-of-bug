import re
import os
import glob
from os import path

def listToString(s):   
    str1 = " "     
    return (str1.join(s))
fields = ["build_name", "package_name", "pakage_link", "file_name", "file_link", "commit_id", "commit_date", "tokens"]
ist = []
num = 1
batch = 1
base_path = "C:/Users/Lenovo/Desktop/JSON/py1/tokens2.txt"
batch_path = "C:/Users/Lenovo/Desktop/JSON/py/batch"
with open (base_path) as in_file:
        for line in in_file:
            ist.append(line.strip())
        print(len(ist))
        with open(batch_path+str(batch)+".txt","a+") as out_file:
            if(os.stat(base_path).st_size+os.stat(batch_path+str(batch)+".txt").st_size>5237760):
                batch = batch+1
                out_file = open(batch_path+str(batch)+".txt","a+")
            out_file.write("{\n\"fields\" : {\n")
            for i in range(len(fields)):
                if(i==len(fields)-1):
                    st = listToString(ist[i:])
                    out_file.write("\t\t\""+fields[i]+"\": [\""+st+"\"]\n},\n")
                else:
                    out_file.write("\t\t\""+fields[i]+"\": \""+ist[i]+"\",\n")
            out_file.write("\"id\" : \""+str(num)+"\",\n\"type\" : \"add\"\n}\n")
        num = num+1
        in_file.close()

            
