from asyncio import get_event_loop
import asyncio
from serial_asyncio import open_serial_connection

async def run():
    reader, writer = await open_serial_connection(url='COM5', baudrate=9600)
    line = await reader.readline()
    print(str(line, 'utf-8'))

async def walk():
    print("init")
    await asyncio.sleep(5)
    print("second message")

async def main():
    task1 = asyncio.create_task(run())
    task2 =  asyncio.create_task(walk())
    await task1
    await task2
    
asyncio.run(main())