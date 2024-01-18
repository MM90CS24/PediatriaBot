from pathlib import Path




file= open("final.png","rb")
asd = file.readlines()

ficherofinal = open("asd.rar","wb")

for e in range(6588,len(asd)):

        ficherofinal.write(asd[e])



ficherofinal.close()
