from os import write
from freeapi import Freeapi



import json


api = Freeapi()
texttfile = open("testo.txt","w")
for a in range(1,4): 

    e=  api.upload_file("iphone.part"+str(a)+".rar")
    texttfile.write(json.dumps({"name":"iphone.part"+str(a)+".rar","url":e}))

    print(e)
texttfile.close()
