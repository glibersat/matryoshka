#!/usr/bin/env python
import pykka
import cocos

from rfoo.utils import rconsole
rconsole.spawn_server()

import matryoshka
from matryoshka.component import Component, Model, Controller, Property, IComponent

class SpriteController(Controller):
    def __init__(self, aSpriteModel, anICharacter):
        super(SpriteController, self).__init__(aSpriteModel)

        self.x = anICharacter
        self.x.subscribe(self)

    def propertychange(self, *args):
        print "update", args
    
class SpriteComponent(Component):
    controller = SpriteController

if __name__ == '__main__':
    zombies = [CharacterComponent('bob', 10, 10), CharacterComponent('alphonse', 20, 30)]

    spr = SpriteComponent(zombies[0])

    while True:
        zombies[0].set_pos(30, 30)
        import time
        time.sleep(2)

    print "shutting down..."

    # matryoshka.component.Registry.stop_all()
    

