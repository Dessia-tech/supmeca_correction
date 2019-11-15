#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 21:37:49 2019

@author: jezequel
"""
import objects

shaft1 = objects.Shaft((0.1, 0.3))
shaft2 = objects.Shaft((0.3, 0.4))
shaft3 = objects.Shaft((0.2, 0.6))

gear1 = objects.Gear(0.1, 0.03)
gear2 = objects.Gear(0.2, 0.05)
gear3 = objects.Gear(0.1, 0.05)

mel = objects.Accessory(0.05, 0.1, 10, 10, 'mel')

drive = objects.Drive(gear1, gear2)

sa1 = objects.ShaftAssembly(shaft1, [gear1], mel)
sa2 = objects.ShaftAssembly(shaft2, [gear2, gear3])

reductor = objects.Reductor([sa1, sa2], [drive])

reductor.plot()