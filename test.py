#!/usr/bin/env python
import pykka
import cocos

from rfoo.utils import rconsole
rconsole.spawn_server()

import matryoshka
from matryoshka.component import Component, Model, Controller, Property, IComponent

class ICharacter(IComponent):
    def set_pos(x, y):
        pass

class CharacterModel(Model):
    x = Property(str, 0)
    y = Property(str, 0)    

class CharacterController(Controller):
    def __init__(self, aCharacterModel, name, x, y, **kwargs):
        super(CharacterController, self).__init__(aCharacterModel)
        self._model.name = name
        self.set_pos(x, y)

    @property
    def x(self):
        return self._model.x

    @x.setter
    def x(self, value):
        self._model.x = value

    @property
    def y(self):
        return self._model.y

    @y.setter
    def y(self, value):
        self._model.y = value

    def set_pos(self, x, y):
        self.x = x
        self.y = y
    
class CharacterComponent(Component):
    matryoshka.component.interface.implements(ICharacter)
    
    model = CharacterModel
    controller = CharacterController


if __name__ == '__main__':
    # actor.tell({'coin': 2})
    # print actor.ask({'command': 'coin'})
    #actor.talk()
    #UI.start().proxy().run()


    zombies = [CharacterComponent('bob', 10, 10), CharacterComponent('alphonse', 20, 30)]

    # Gtk.main()
    while True:
        print "alive"
        import time
        time.sleep(2)

    matryoshka.Registry.stop_all()
    

class UI(pykka.ThreadingActor):
    def run(self):
        cocos.director.director.init()        
        layer = Hello()
        label = cocos.text.Label('Hello, world',
                                 font_name='Times New Roman',
                                 font_size=32,
                                 anchor_x='center', anchor_y='center')
        label.position = (320, 240)
        layer.add(label)
        scene = cocos.scene.Scene(layer)
        cocos.director.director.run(scene)
