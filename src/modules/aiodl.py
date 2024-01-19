import aiohttp
from yarl import URL
from pyrogram.types import Message

async def aio(url: str, msg: Message):
    # Se puede usar este:
    # filename = url.split('/')[-1]
    # o este:
    filename = URL(url).name # Recomendado
    lastsize = ""
    await msg.edit("Descargando "+str(filename))
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=None) as response:
            try:
             total_length = int(response.headers.get('content-length'))
            except:
                print("no se pudo determinar longitud")
            total = 0
            with open(filename, 'wb') as f:
                while True:
                    chunk = await response.content.read(1024)
                    total+=len(chunk)
                    if not chunk:
                        break
                    f.write(chunk)
                    f.flush()

    print('\nDownload complete!')

    return filename