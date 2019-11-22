#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 21:37:49 2019

@author: jezequel
"""
from objects_enhanced_babylon import Accessory, Gear, Drive, Reductor, ShaftAssembly, Shaft
from optimization import Optimizer
from itertools import product, permutations, combinations
#import matplotlib.pyplot as plt
#from matplotlib import patches

engine = Accessory(diameter=0.30, length=0.050, speed=4000, name='Engine')
accessories = [Accessory(diameter=0.15, length=0.050, speed=2000, name='Fuel Pump'),
               Accessory(diameter=0.12, length=0.050, speed=3500, name='Starter')]

shaft0 = Shaft(0, 0)
gear0 = Gear(0.010, 0.010)

shaft1 = Shaft(0.0075, 0)

gear11 = Gear(0.005, 0.010)
gear12 = Gear(0.015, 0.010)

shaft2 = Shaft(0.0075+0.025, 0)
gear2 = Gear(0.010, 0.010)

sa0 = ShaftAssembly(shaft0, [gear0], engine)
sa1 = ShaftAssembly(shaft1, [gear11, gear12], accessories[0])
sa2 = ShaftAssembly(shaft2, [gear2], accessories[1])

drive0 = Drive(gear0, gear11)
drive1 = Drive(gear12, gear2)


reductor = Reductor([sa0, sa1, sa2], [drive0, drive1])
limits = {'minimum' : {'x' : 0.2, 'y' : 0.05},
          'maximum' : {'x' : 0.4, 'y' : 0.3}}

optimizer = Optimizer(reductor=reductor, limits=limits)

res = optimizer.minimize(1000)
print(res.success)
print([gear.diameter for sa in optimizer.reductor.shaft_assemblies for gear in sa.gears])
print(optimizer.reductor.speeds())

optimizer.reductor.plot()
