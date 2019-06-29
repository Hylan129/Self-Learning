import tkinter
import time
from greenlet import greenlet
import threading
import os

root = tkinter.Tk()
root.minsize(300,200)
root.maxsize(300,200)
root.title("Hylan 测试中")
button1= tkinter.Button(root,text="点击开始",command=lambda:start_test(t1))
button1.place(x=100,y=50,width=60,height=30)

button2= tkinter.Button(root,text="点击结束",command=lambda:kill())
button2.place(x=100,y=120,width=60,height=30)

def run():
    for i in range(10000):
        print(i)
        time.sleep(0.2)
        

def default():
     for i in range(10000):
        print(i*10)
        time.sleep(0.2)

threads = []
t1 = threading.Thread(target=run)

#threads.append(t1)

#t2 = threading.Thread(target=port_close2)
#threads.append(t2)


#t.setDaemon(True)
#t.start()
        
def start_test(self):
    if self._started.is_set():
        print(self._started.is_set())
        #print(self._started._Flag)
        self._started.clear()
        self._started.__init__()
        print(self._started.is_set())
        print(self._started.set())
        self._started.clear()
        _sys.exc_clear()
        self.start()
        print(self._started.set())

        
    else:
        self.start()
    

import inspect
import ctypes
 
def _async_raise(tid, exctype):
    """raises the exception, performs cleanup if needed"""
    tid = ctypes.c_long(tid)
    if not inspect.isclass(exctype):
        exctype = type(exctype)
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
    if res == 0:
        raise ValueError("invalid thread id")
    elif res != 1:
        # """if it returns a number greater than one, you're in trouble,
        # and you should call it again with exc=NULL to revert the effect"""
        ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        raise SystemError("PyThreadState_SetAsyncExc failed")
 
def stop_thread(thread):
    _async_raise(thread.ident, SystemExit)
    
def kill():
    stop_thread(t1)

    
'''

gr1 = greenlet(run)
gr2 = greenlet(default)

def start():
    gr1.switch()
'''
