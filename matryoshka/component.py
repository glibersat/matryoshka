#!/usr/bin/env python
import pykka.gevent

from metamodel import SubscribableModel
from metamodel import Property

import zope.interface as interface
from zope.interface import Interface
from zope.interface.verify import verifyObject
from zope.component import provideUtility

class IComponent(Interface):
    pass

class Controller(pykka.gevent.GeventActor):
    """
    A living controller (a thread or greenlet) that act as the
    single point of synchronization for the whole component.
    """
    def __init__(self, aModel):
        super(Controller, self).__init__()
        self.model = aModel

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

        # Check interface declaration integrity        
        for itf in interface.implementedBy(type(self)):
            verifyObject(itf, self)
            provideUtility(self, itf)

    def __getattr__(self, name):
        """
        Try to get the name from the component, otherwise, hit the
        Model
        """
        try:
            return super(Component, self).__getattr__(name)
        except AttributeError:
            return getattr(self._model, name)

class Registry(object):
    @classmethod        
    def stop_all(self):
        pykka.ActorRegistry.stop_all()

