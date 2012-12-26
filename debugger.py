from matryoshka import Debugger
from test import CharacterComponent
from gi.repository import Gtk
import gc

import rfoo

def start():
    comps = []
    for obj in gc.get_objects():
        try:
            if 'CharacterComponent' in obj.__class__.__name__:
                comps.append(obj)
        except:
            pass
            
    print "yeah", comps
    win = Debugger(comps)
    win.show_all()    
    Gtk.main()


if __name__ == '__main__':
    conn = rfoo.InetConnection().connect(port=54321)
    rfoo.Proxy(conn).runsource("""import debugger; debugger.start()""")
