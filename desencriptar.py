
import asyncio
from json.encoder import JSONEncoder
from PIL import Image
import os
import json
import time
import aiohttp
import requests
from yarl import URL

async def aio(url: str):
    # Se puede usar este:
    # filename = url.split('/')[-1]
    # o este:
    try:
        filename = ""
        with requests.Session() as session:
            data = {"source":"","username": "ernestico1575" ,"password": "291203Er*"}

            session.headers.update({"Content-Type":"application/x-www-form-urlencoded"})
        
            with session.post(url="https://revsaludpublica.sld.cu/index.php/spu/login/signIn",data=data)as login:
                print(login.url)
                with session.get(url, timeout=10,stream =True) as response:
                
                    total_length = int(response.headers.get('content-length'))
                    namesplit = response.headers.get('Content-Disposition').split(';')
                    asd = namesplit[len(namesplit)-1]
                    espacioname = asd.split('=')
                    finalname = espacioname[1].split('"')
                    filename = finalname[1]
            
                
                    with open(filename, 'wb') as f:

                     for a in response.iter_content(chunk_size=6096):
                            if (len(a)==0):
                                    break
                            f.write(a)
                            f.flush()
                            
                        
                            print('\r{:.2f}%'.format(f.tell() * 100 / total_length), end='')
    except:
        
        print("Time out it try again \n")

        time.sleep(10)

        await aio(url)
        
                        

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

                time.sleep(2)
                jsond =json.loads(line)
                print("Descargando "+ str(jsond["name"]))


                filenames = await aio(jsond['url'])

                copiados = 0 
                estado = True
                if(not os.path.isdir("Descarga/"+jsond["name"].split(".")[0])):
                 os.mkdir("Descarga/"+jsond["name"].split(".")[0])
                ficherofinal= open("Descarga/"+jsond["name"].split(".")[0]+"/"+jsond['name'],'wb')

                file= open(filenames,"rb")
                filen = file.readlines()

                for e in range(6589,len(filen)):

                    ficherofinal.write(filen[e])

                print("Se descifro correctamente " + jsond['name'] + "\n")

                file.close()   

                os.remove(filenames)
                
                ficherofinal.close()

asyncio.run( Descargar())
