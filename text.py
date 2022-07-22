from asyncio import get_event_loop
import asyncio
from serial_asyncio import open_serial_connection

async def run():
    reader, writer = await open_serial_connection(url='COM5', baudrate=9600)
    while True:
        line = await reader.readline()
        print(str(line, 'utf-8'))

asyncio.new_event_loop().run_until_complete(run())