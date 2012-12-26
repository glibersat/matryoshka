#!/usr/bin/env python
import pykka

from metamodel import SubscribableModel
from metamodel import Property

import zope.interface as interface

class IComponent(interface.Interface):
    pass

class Controller(pykka.ThreadingActor):
    """
    A living controller (a thread or greenlet) that act as the
    single point of synchronization for the whole component.
    """
    def __init__(self, aModel):
        super(Controller, self).__init__()
        self._model = aModel

class Model(SubscribableModel):
    name = Property(str, 'unnamed')
    
class Component(pykka.proxy.ActorProxy):
    """
    A simple component that has:
     - a controller
     - a model
    """
    model = Model
    controller = Controller

    interface.implements(IComponent)
    
    def __init__(self, *args, **kwargs):
        self._model = self.model()
        self._controller = self.controller.start(self._model, *args, **kwargs)
        
        super(Component, self).__init__(self._controller)

    def __getattr__(self, name):
        """
        Try to get the name from the component, otherwise, hit the
        Model
        """
        try:
            return super(Component, self).__getattr__(name)
        except AttributeError:
            return getattr(self._model, name)
            
from gi.repository import Gtk

class Debugger(Gtk.Window):
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


class Registry(object):
    @classmethod        
    def stop_all(self):
        pykka.ActorRegistry.stop_all()

