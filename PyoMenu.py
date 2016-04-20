#Embedded file name: PyoMenu.py
import os
import Tkinter as tk
from functools import partial
import subprocess
import time
import webbrowser
os.chdir(os.path.dirname(os.path.realpath(__file__)))
scriptlist = []
for filename in os.listdir('.'):
    if filename.endswith('.pyoc'):
        scriptlist.extend([filename])

p = None
pi = None
pn = None

def FormatFileName(fname):
    tmp = fname.replace('_', ' ')
    if tmp.endswith('.py'):
        tmp = tmp[:-3]
    if tmp.endswith('.pyoc'):
        tmp = tmp[:-5]
    return tmp


def QuitCurrentScript():
    global p
    global pi
    global btns
    if p != None:
        if p.poll() == None:
            p.terminate()
            time.sleep(0.5)
        if p.poll() == None:
            p.kill()
            time.sleep(0.5)
        if p.poll() == None:
            return False
    if pi != None:
        btns[pi].configure(background='gray95', relief=tk.RAISED)
        pi = None
        pn = None
    return True


def CallScript(i):
    global p
    global scriptlist
    if p != None:
        if p.poll() == None:
            return False
    if i >= len(scriptlist):
        return False
    sf = scriptlist[i]
    p = subprocess.Popen(['python', sf])
    print 'pid: ' + str(p.pid)
    return True


def ActivateScript(arg):
    global pi
    global pn
    if arg < len(scriptlist):
        prev_pi = pi
        if QuitCurrentScript() == False:
            print 'Error: could not terminate previous script'
            return False
        if prev_pi != arg:
            if CallScript(arg) == False:
                print 'Error: could not call script'
                return False
            else:
                pi = arg
                pn = scriptlist[arg]
                btns[pi].configure(background='#50BBE7', relief=tk.SUNKEN)
                return True
    else:
        print 'Error: script index out of scriptlist'
        return False


def Close():
    global root
    QuitCurrentScript()
    root.quit()


def AboutBox():
    webbrowser.open('http://www.fernandocosentino.net/pyoconnect')


root = tk.Tk()
root.title('PyoConnect v1.0')
main = tk.Frame(root, width=300, height=300, background='gray95')
main.pack(fill=tk.BOTH, expand=1)
topframe = tk.Frame(main, width=300, height=50, padx=10, pady=10, background='gray20')
topframe.pack_propagate(0)
topframe.pack(fill=tk.BOTH)
toplabel = tk.Label(topframe, text='PyoConnect', background='gray20', foreground='#50BBE7', font='Arial 20')
toplabel.pack(fill=tk.BOTH)
btnframe = tk.Frame(main, width=280, padx=10, pady=10, background='gray95')
btnframe.pack(fill=tk.X)
i = 0
btns = []
for sfile in scriptlist:
    btns.extend([tk.Button(btnframe, text=FormatFileName(sfile), background='gray95', border=0, relief=tk.RAISED)])
    btns[i].config(command=partial(ActivateScript, i))
    btns[i].scriptname = sfile
    btns[i].script_id = i
    btns[i].pack(fill=tk.X)
    i += 1

tk.Label(btnframe, text=' ', background='gray95').pack()
tk.Button(btnframe, text='About', background='#50BBE7', border=0, command=AboutBox).pack(side=tk.LEFT)
tk.Button(btnframe, text='Quit', background='#50BBE7', border=0, command=Close).pack(side=tk.RIGHT)
root.mainloop()
try:
    root.destroy()
except:
    pass
