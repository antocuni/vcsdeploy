import os
import py

DIR = py.path.local(__file__).dirpath()

def check(in_, out):
    return out.check(exists=False) or in_.stat().mtime > out.stat().mtime

def make():
    for ui in DIR.visit('*.ui'):
        pyname = 'Ui_' + ui.basename.replace('.ui', '.py')
        pyname = py.path.local(pyname)
        if check(ui, pyname):
            print ui
            os.system('pyuic4 "%s" -o "%s"' % (ui, pyname))

    for rc in DIR.visit('*.qrc'):
        pyname = rc.basename.replace('.qrc', '_rc.py')
        pyname = py.path.local(pyname)
        if check(rc, pyname):
            print rc
            os.system('pyrcc4 "%s" -o "%s"' % (rc, pyname))


make()
