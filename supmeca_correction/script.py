#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 21:37:49 2019

@author: jezequel
"""
from objects import Accessory, Gear, Drive, Reductor, ShaftAssembly, Shaft, Generator
from optimization import Optimizer
import matplotlib.pyplot as plt
from matplotlib import patches

engine = Accessory(diameter=0.30, length=0.050, speed=4000, name='Engine')
accessories = [Accessory(diameter=0.15, length=0.050, speed=2000, name='Fuel Pump'),
               Accessory(diameter=0.12, length=0.050, speed=3500, name='Starter'),
               Accessory(diameter=0.18, length=0.050, speed=750, name='Oil Pump')]

generator = Generator(engine, accessories)

limits = {'minimum' : {'x' : 0.2, 'y' : 0.05},
          'maximum' : {'x' : 0.7, 'y' : 0.3}}

results = []
for reductor in generator.reductors:
    optimizer = Optimizer(reductor=reductor, limits=limits)

    res = optimizer.minimize(1000)
    print(res.success)
    print([gear.diameter for sa in optimizer.reductor.shaft_assemblies for gear in sa.gears])
    print(optimizer.reductor.speeds())
    results.append(optimizer.reductor)
