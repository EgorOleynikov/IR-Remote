import serial
from tkinter import *
from tkinter import ttk
import asyncio
from serial_asyncio import open_serial_connection


ARDUINO_CONF = {"port": "COM5", "baudrate":"9600"};

# UI section
root = Tk()
root.title("Remote")

content = ttk.Frame(root)
frame = ttk.Notebook(content, width=700, height=600)
page1 = ttk.Frame(frame)   # first page, which would get widgets gridded into it
page2 = ttk.Frame(frame)   # second page
frame.add(page1, text='One')
frame.add(page2, text='Two')

#vars for buttons
onevar = BooleanVar(value=True)
twovar = BooleanVar(value=False)
threevar = BooleanVar(value=True)
#

#funcs
async def arduino_request(value):
    #value[1].write(bytearray(1)) # awakes arduino 
    line = await value[0].readline()
    print(line)
    #value[1].write(bytearray(0))

async def popUp_waitForReadings():
    reader, writer = await open_serial_connection(url=ARDUINO_CONF["port"], baudrate=ARDUINO_CONF["baudrate"])
    def dismiss():
        #writer.write(bytearray(0))
        dlg.grab_release()
        dlg.destroy()
    
    dlg = Toplevel(root)
    ttk.Button(dlg, text="Done", command=dismiss).grid()
    dlg.protocol("WM_DELETE_WINDOW", dismiss) # intercept close button
    dlg.transient(root)   # dialog window is related to main
    dlg.wait_visibility() # can't grab until window appears, so we wait
    dlg.grab_set()        # ensure all input goes to our window
    #dlg.wait_window()     # block until window is destroyed
    return [reader, writer]

async def main():
    task1 = asyncio.create_task(popUp_waitForReadings())
    value = await task1
    task2 = asyncio.create_task(arduino_request(value))
    await task2
    

#

#define members
#p1
one = ttk.Checkbutton(page1, text="One", variable=onevar, onvalue=True)
two = ttk.Checkbutton(page1, text="Two", variable=twovar, onvalue=True)
three = ttk.Checkbutton(page1, text="Three", variable=threevar, onvalue=True)
#
#p2
dataName = ttk.Entry(page2)
add = ttk.Button(page2, text="Add", command=lambda: asyncio.run(main()))
#
#

#initial
content.grid(column=0, row=0)
frame.grid(column=0, row=0, columnspan=3, rowspan=2)
#
#p1 layout
one.grid(column=0, row=1)
two.grid(column=0, row=2)
three.grid(column=0, row=3)
#
#p2 layout
dataName.grid(column=0, row=0)
add.grid(column=1, row=0)
#

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
content.columnconfigure(0, weight=3)
content.columnconfigure(1, weight=3)
content.columnconfigure(2, weight=3)
content.columnconfigure(3, weight=1)
content.columnconfigure(4, weight=1)
content.rowconfigure(1, weight=1)

root.mainloop()
#

# arduino section
# ser = serial.Serial(port="COM5", baudrate=9600)  # open serial port
# print(ser.name)         # check which port was really used
# res = ser.read_all()
# ser.close()
# print(res)
#
