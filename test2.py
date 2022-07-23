import threading
from time import sleep

def foo():
    print("dick")
    sleep(1)
    print("dick2")

x = threading.Thread(target=foo)
x.start()

print("init")
sleep(3)
print("init2")