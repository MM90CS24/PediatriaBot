
import asyncio
from json.encoder import JSONEncoder
from PIL import Image
import os
import json
import aiohttp
import requests
from yarl import URL
async def aio(url: str):
    # Se puede usar este:
    # filename = url.split('/')[-1]
    # o este:
    filename = ""
    with requests.Session() as session:
        data = {"source":"","username": "ernestico1575" ,"password": "12345678"}

        session.headers.update({"Content-Type":"application/x-www-form-urlencoded"})

        with session.post(url="https://revpediatria.sld.cu/index.php/ped/login/signIn",data=data)as login:
            print(login.url)
            with session.get(url, timeout=None,stream =True) as response:
              
                total_length = int(response.headers.get('content-length'))
                namesplit = response.headers.get('Content-Disposition').split(';')
                asd = namesplit[len(namesplit)-1]
                espacioname = asd.split('=')
                finalname = espacioname[1].split('"')
                filename = finalname[1]
          
               
                with open(filename, 'wb') as f:
                    for a in response.iter_content(chunk_size=4096):
                        if not a:
                            break
                        f.write(a)
                        f.flush()
                    
                        print('\r{:.2f}%'.format(f.tell() * 100 / total_length), end='')
                    

    print('\nDownload complete!')

    return filename
async def Descargar():
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

        
            jsond =json.loads(line)
    
        
            print("Descargando "+ str(jsond["name"]))
            filenames = await aio(jsond['url'])


            copiados = 0 
            estado = True
            ficherofinal= open("Descarga/"+jsond['name'],'wb')
            file= open(filenames,"rb")
            while estado: 
                
              

                datos = file.read(4096)

                copiados += len(datos)

                if(len(datos) == 0):
                    estado = False
                    break
                
                if(copiados > 1971322):

                    print("va por el byte "+str(copiados))

                    ficherofinal.write(datos)
                    

            ficherofinal.close()
            file.close()

            os.remove(filenames)
            return "correcto"

asyncio.run( Descargar())
