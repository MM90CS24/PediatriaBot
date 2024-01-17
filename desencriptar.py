
from json.encoder import JSONEncoder
from PIL import Image
import os
import json
import aiohttp
from yarl import URL
async def aio(url: str):
    # Se puede usar este:
    # filename = url.split('/')[-1]
    # o este:
    filename = URL(url).name # Recomendado
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=None) as response:
            try:
             total_length = int(response.headers.get('content-length'))
            except:
                print("no se pudo determinar longitud")
            with open(filename, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    if not chunk:
                        break
                    f.write(chunk)
                    f.flush()
                  
                    print('\r{:.2f}%'.format(f.tell() * 100 / total_length), end='')
                    

    print('\nDownload complete!')

    return filename

files = os.listdir("Descarga")
filestxt = list()

for file in files:
    splites = file.split('.')
    if(splites[len(splites)-1] == "txt"):
        filestxt.append(file)

for filedes in filestxt:
    txtfile = open("Descarga/"+filedes,"r")

    lines = txtfile.readlines()
    for line in lines:

        lisa = list(line)
        for e in lisa:
            if(e == "'"):
                lisa[lisa.index(e)] = '"'
            if(e =='"'):
                lisa[lisa.index(e)] = "'"
        finalisa  = ""
        for ea in lisa:
            finalisa += ea
            
        lisa = finalisa
        jsond =json.JSONDecoder().decode(line) 
   
     

        filenames = aio(jsond['url'])


        copiados = 0 
        estado = True

        while estado: 
            ficherofinal= open(jsond['name'],'wb')

            datos = open(filenames,"rb")

            datos = file.read(1024)

            copiados += len(datos)

            if(len(datos) == 0):
                estado = False
                break
            
            if(copiados > 1971322):

                print("va por el byte "+str(copiados))

                ficherofinal.write(datos)
                

        ficherofinal.close()
        os.remove(filenames)
   
