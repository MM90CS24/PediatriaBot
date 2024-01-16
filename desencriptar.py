
from PIL import Image


file = open("final.png",'rb')

ficherofinal = open("testa.rar","wb")
fotorestaura = open("fotorestaura.png","wb")
copiados = 0 

estado = True

while estado: 

 datos = file.read(1024)

 copiados += len(datos)

 if(len(datos) == 0):
    estado = False
    break
 
 if(copiados > 1971322):

    print("va por el byte "+str(copiados))

    ficherofinal.write(datos)

 else:

    fotorestaura.write(datos)
  
        

ficherofinal.close()
fotorestaura.close()