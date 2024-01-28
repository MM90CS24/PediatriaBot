from genericpath import exists
import json
import os
from pathlib import Path
from pyrogram import Client, filters
from pyrogram.types import Message

from src.cfgs.bot_conf import NAME, HASH, ID, BOT_TK, ZIPS, ALLOWED
from freeapi import Freeapi
from src.modules.aiodl import aio
from src.modules.makezip import compress
from flask import Flask
from threading import Thread
bot: Client = Client(
    name=NAME,
    api_hash=HASH,
    api_id=ID,
    bot_token=BOT_TK
)

@bot.on_message(filters.command("start", prefixes="/"))
async def start(client: Client, message: Message):
    print("Uso el bot "+client.name)
    if message.from_user.id in ALLOWED:
        await message.reply("Hola {} bienvenido al bot para subir a pediatria :v".format(message.from_user.first_name))
    else:
        await message.reply("No tiene autorizacion")

@bot.on_message(filters.command("setnube", prefixes="/"))
async def start(client: Client, message: Message):
    print("Uso el bot "+client.name)
    if message.from_user.id in ALLOWED:

        messagesplite = message.text.split(" ")[-1]
        file = open(str(message.from_user.id)+".json","w")
        file.write(messagesplite)
        file.close()

        await message.reply("tu configuracion actual es : " +str(open(str(message.from_user.id)+".json","r").read()))

    else:
        await message.reply("No tiene autorizacion")


@bot.on_message(filters.regex(".*https://.*") | filters.regex(".*http://.*"))
async def download(client: Client, message: Message):
    
    if message.from_user.id in ALLOWED:
        print("Uso el bot "+client.name)
        passw=""
        user=""
        nube= ""
        try:

             jsonloads = json.loads(open(str(message.from_user.id)+".json","r").read())
             passw = jsonloads["pass"]
      
             user= jsonloads["username"]
          
             nube = jsonloads["nube"]
    

        except:
            await message.reply("Configura tu nube con /setnube {'nube':'sunube','username':'nombredeusuario','pass':'contrasena'}")

        links = message.text.split("\n")

        for e in links:
            Free_API = Freeapi(nube,user,passw)
            if(e==None):
                continue
            msg = await message.reply("Link directo Detectado")
            filename = ''
            size = 0
            try :
                filename = await aio(e, msg)
                size = Path(filename).stat().st_size
            except:
            
                filename = e.split('/')
                
                filename = filename[len(filename)-1]
    
                size = Path(filename).stat().st_size

        

            await msg.edit("Descargado ```{}```\nTamaño: ```{:.2f} MB```".format(filename, size / 1000000))
            
            try:
                if size > ZIPS * 1024 * 1024:

                    comp_msg = await message.reply("El archivo pesa mas de lo esperado, se comprimira")
                    file_list = compress(filename, part_size=ZIPS)
                    
                    
                    fin_msg = await comp_msg.edit("Archivo Comprimido en partes de {} MB\n\nAhora subiendo".format(ZIPS))
                    
                    for files in file_list:

                        await message.reply("Subiendo "+ files)
               
                     
                                               
                        link =  Free_API.upload_file(files)



                        with open(filename+".txt", "a") as txt:
                            txt.write(str(json.dumps({"name":files,"url":link,"username":str(Free_API.returnusername()),"pass":str(Free_API.returnpass())})+"\n"))
                        os.remove(files)
                        
                    try:
                        os.remove(filename)
                    except:
                        print("ya no existe")
                    await message.reply_document(filename+".txt", caption="Archivo de [{}](https://t.me/{})".format(message.from_user.first_name, message.from_user.username))
                    
    

                    await fin_msg.delete()
                    await message.reply("Subido ```{}```".format(filename))

                else:
                    filecompresed = compress(filename,size)
                    
                    txt = open(filename+".txt","w")

                    Free_API = Freeapi()
                    file_link = Free_API.upload_file(filecompresed[0])

                    txt.write(json.dumps({"url": file_link, "name":filecompresed[0],"username":str(Free_API.returnusername()),"pass":str(Free_API.returnpass())}))
                    txt.close()

                    await message.reply_document(filename+".txt")
                    await message.reply(str(filecompresed))

                    await message.reply(file_link)

                    
                    os.remove(filename+".txt")
                    try:
                        os.remove(filename)
                    except:
                        print("ya no existe")
                    os.remove(filecompresed[0])
                    os.remove(filecompresed[0]+".jpg")
                    
    

            except Exception as e:
                await message.reply(e)
                # os.remove(filename)
                pass
    else:
        await message.reply("No tiene autorizacion")

if __name__ == "__main__":
    # print("Iniciando Bot")
    # bot.start()
    # print("Bot Iniciado")
    # bot.loop.run_forever()
    app = Flask(__name__)

    @app.route('/')
    def index():
         return "Alive"

    def run():
     app.run(host='0.0.0.0', port=10000)

    def keep_alive():
     t = Thread(target=run)
     t.start()
     
    keep_alive()
    print("Bot iniciado")
    bot.run()
    