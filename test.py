from freeapi import Freeapi

api = Freeapi()


files = open("final.png","wb")

files.write(open("Rincon.png",'rb').read()+open("test.rar","rb").read())

files.close()