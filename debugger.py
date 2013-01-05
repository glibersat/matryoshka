from matryoshka.debugger import GtkDebugger
from gi.repository import Gtk
import gc

import rfoo

def start():
    comps = []
    for obj in gc.get_objects():
        try:
            if 'Component' in obj.__class__.__name__:
                comps.append(obj)
        except:
            pass
            
    win = GtkDebugger(comps)
    win.show_all()    
    Gtk.main()


if __name__ == '__main__':
    conn = rfoo.InetConnection().connect(port=54321)
    rfoo.Proxy(conn).runsource("""import debugger; debugger.start()""")
