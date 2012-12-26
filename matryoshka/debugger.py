from gi.repository import Gtk

class GtkDebugger(Gtk.Window):
    def __init__(self, aComponentList):
        Gtk.Window.__init__(self, title='Debugger')
        self.connect("delete-event", Gtk.main_quit)

        self.store = Gtk.TreeStore(str)

        for comp in aComponentList:
            p = self.store.append(None, [comp.name])
            self.store.append(p, [str(comp._model)])
            self.store.append(p, [str(comp._controller)])            


        tree = Gtk.TreeView(self.store)
        renderer = Gtk.CellRendererText()
        column = Gtk.TreeViewColumn("Name", renderer, text=0)
        tree.append_column(column)

        self.add(tree)
