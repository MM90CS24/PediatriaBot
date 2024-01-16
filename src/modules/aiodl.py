import aiohttp
from yarl import URL
from pyrogram.types import Message

async def aio(url: str, msg: Message):
    # Se puede usar este:
    # filename = url.split('/')[-1]
    # o este:
    filename = URL(url).name # Recomendado
    await msg.edit("Descargando ```{}```".format(filename))
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=None) as response:
            total_length = int(response.headers.get('content-length'))
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