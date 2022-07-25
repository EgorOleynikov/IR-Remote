from base64 import encode
from os import path
import threading
from tkinter import messagebox
import serial
import json
from tkinter import *
from tkinter import ttk
#import asyncio
#from serial_asyncio import open_serial_connection


ARDUINO_CONF = {"port": "COM5", "baudrate":"9600"};

# UI section
root = Tk()
root.title("Remote")

# Gets the requested values of the height and widht.
windowWidth = root.winfo_reqwidth()
windowHeight = root.winfo_reqheight()
#print("Width",windowWidth,"Height",windowHeight) 
# Gets both half the screen width/height and window width/height
positionRight = int(root.winfo_screenwidth()/2 - windowWidth/2)
positionDown = int(root.winfo_screenheight()/2 - windowHeight/2) 
# Positions the window in the center of the page.
root.geometry("+{}+{}".format(positionRight, positionDown))

content = ttk.Frame(root)
frame = ttk.Notebook(content, width=700, height=600)
page1 = ttk.Frame(frame)  # first page, which would get widgets gridded into it
page2 = ttk.Frame(frame)   # second page
frame.add(page1, text='Send')
frame.add(page2, text='Receive')

#vars for buttons
onevar = BooleanVar(value=True)
twovar = BooleanVar(value=False)
threevar = BooleanVar(value=True)
entryNameVar = StringVar()
#

#funcs

# def listbox_update(jsonDict):


def popUp_waitForReadings():
    global fileJson
    entryName = entryNameVar.get()
    if len(entryName) > 0:
        if "♂" in entryName:
            messagebox.showwarning(message='WARNING!!!\nArtem detected', title="Gay alert")

        if entryName in fileJson:
            messagebox.showerror(message='Name is already taken')
            return
        
        dlg = Toplevel(root)
        label = ttk.Label(dlg)            
        
        try:
            ser = serial.Serial(ARDUINO_CONF["port"], ARDUINO_CONF["baudrate"])
            label['text'] = "Connection established"
        except:
            label['text'] = "Port error"
            #raise Exception("Port " + ARDUINO_CONF["port"] + " error")

        def arduino_request(): # runs in a separate thread
            def serial_read():
                try:
                    respond = ser.readline() # reads last line
                    respond = respond.decode().replace("\r\n", "")
                    return respond
                except:
                    raise Exception("Error has occurred")

            def serial_write(message):
                try:
                    ser.write(message.encode()) # reads last line
                except:
                    raise Exception("Error has occurred")
            
            respond = serial_read()
            print(respond)
            if respond == "Ready":
                # ready
                serial_write("1") # awakes arduino
                respond = serial_read()
                print(respond)
                if respond == "Listen":
                    # listen
                    label['text'] = "Listening for IR data"
                    decode = serial_read()
                    print(decode)
                    rawData = serial_read()
                    print(rawData)
                    label["text"] = "Gathered"
                    dlg.destroy()
                    with open("settings.json", "w+") as file:
                        fileJson.update({entryName: {"decode": decode, "rawData": rawData}})
                        print(fileJson)
                        json.dump(fileJson, file, indent=4, separators=(',', ': '))
                        fileJsonKeys.append(entryName)
                        choicesvar.set(fileJsonKeys)

                
            serial_write("0")
        
        def dismiss():
            dlg.grab_release()
            dlg.destroy()
            # ser.cancel_read()
            # ser.cancel_write()
            ser.close()

        thread = threading.Thread(target=arduino_request, args=())
        thread.start()
        
        # Gets both half the screen width/height and window width/height
        positionRight = int(dlg.winfo_screenwidth()/2 - 200/2)
        positionDown = int(dlg.winfo_screenheight()/2 - 100/2)
        # Positions the window in the center of the page.
        dlg.geometry("200x100+{}+{}".format(positionRight, positionDown))

        #label.place(relx=0.5, rely=0.3, anchor=CENTER)
        #ttk.Button(dlg, text="Cancel", command=dismiss).place(relx=0.5, rely=0.7, anchor=CENTER)
        label.grid(column=0, row=0)
        ttk.Button(dlg, text="Cancel", command=dismiss).grid(column=0, row=1)

        dlg.columnconfigure(0, weight=1)
        dlg.rowconfigure(0, weight=1)
        dlg.rowconfigure(1, weight=1)
        dlg.protocol("WM_DELETE_WINDOW", dismiss) # intercept close button
        dlg.transient(root)   # dialog window is related to main
        dlg.wait_visibility() # can't grab until window appears, so we wait
        dlg.grab_set()        # ensure all input goes to our window
        dlg.wait_window()     # block until window is destroyed

    else:
        messagebox.showinfo(message='Entry must have a name')

#

#define members
#p1
one = ttk.Checkbutton(page1, text="One", variable=onevar, onvalue=True)
two = ttk.Checkbutton(page1, text="Two", variable=twovar, onvalue=True)
three = ttk.Checkbutton(page1, text="Three", variable=threevar, onvalue=True)
#
#p2
labelEntry = ttk.Label(page2, text="Add new entry")
dataName = ttk.Entry(page2, textvariable=entryNameVar)
btnAdd = ttk.Button(page2, text="Add", command=lambda: popUp_waitForReadings())
labelArea = ttk.Label(page2, text="Records")
labelRight = ttk.Label(page2, text="placeholder")
btnRetake = ttk.Button(page2, text="Retake")
btnDel = ttk.Button(page2, text="Delete")
#listbox
fileJson = {}
fileJsonKeys = []
choicesvar = StringVar()
try:
    if path.isfile("settings.json") is True:
        with open("settings.json", "r") as file:
            fileJson = json.load(file)
            fileJsonKeys = list(fileJson.keys())
            choicesvar = StringVar(value=fileJsonKeys)
except:
    pass

#choices = ["apple", "orange", "banana"]
listbox = Listbox(page2, height=15, listvariable=choicesvar)
scrollbar = ttk.Scrollbar(page2, orient=VERTICAL)
listbox["yscrollcommand"] = scrollbar.set
#
#
#

#initial
content.grid(column=0, row=0)
frame.grid(column=0, row=0, columnspan=3, rowspan=2)
root.eval('tk::PlaceWindow . center')
#
#p1 layout
one.grid(column=0, row=1)
two.grid(column=0, row=2)
three.grid(column=0, row=3)
#
#p2 layout
page2.columnconfigure(0, weight=20)
page2.columnconfigure(1, weight=20)
page2.columnconfigure(2, weight=30)
page2.columnconfigure(3, weight=30)
page2.rowconfigure(0, weight=20)
page2.rowconfigure(1, weight=20)
page2.rowconfigure(2, weight=20)
page2.rowconfigure(3, weight=40)
page2.rowconfigure(4, weight=40)

labelEntry.grid(column=0, row=0, columnspan=2)
dataName.grid(column=0, row=1)
btnAdd.grid(column=1, row=1)
labelArea.grid(column=0, row=2, columnspan=2)
listbox.grid(column=0, row=3, columnspan=2, rowspan=2, sticky=(N,W,E,S))
scrollbar.grid(column=2, row=3, rowspan=2, sticky=(N,W,S))
labelRight.grid(column=2, row=3, columnspan=2)
btnRetake.grid(column=2, row=4)
btnDel.grid(column=3, row=4)
#

root.mainloop()

#
