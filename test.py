from freeapi import Freeapi



files = open("final.png","wb")

files.write(open("Rincon.png",'rb').read()+b'\n//aqui\n'+open("iphone.rar","rb").read())

files.close()