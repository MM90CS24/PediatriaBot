from pathlib import Path


copiados = 0 
         
estado = True
ficherofinal= open("asdf.mp4",'wb')

file= open("5785-21615-1-SP.001","rb")

size = Path("5785-21615-1-SP.001").stat().st_size

while estado: 
        


        datos = file.read(4096)

        copiados += len(datos)

        if(len(datos) == 0):
                    estado = False
                    break
                
        if(copiados >= 1971322):

         print("va por el byte "+str(copiados))

         ficherofinal.write(datos)
                    

ficherofinal.close()
