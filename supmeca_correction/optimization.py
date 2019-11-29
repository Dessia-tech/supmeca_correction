#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 14 12:10:01 2019

@author: jezequel
"""
from scipy.optimize import minimize
import numpy as npy

class Optimizer:
    def __init__(self, reductor, limits):
        self.reductor = reductor
        self.limits = limits

        bounds = []
        for shaft_assembly in reductor.shaft_assemblies:
            for gear in shaft_assembly.gears:
                bounds.append([0.05, 7])
        self.bounds = npy.array(bounds)

        self.output_objectives = [sa.accessory.speed for sa in reductor.shaft_assemblies]

    def update(self, x):
        self.reductor.update(x)

    def objective(self, x):
        self.update(x)
        speeds = self.reductor.speeds()
        fonctionnelle = 0
        for i_arbre, speed in enumerate(speeds):
            fonctionnelle += (self.output_objectives[i_arbre] - speed)**2

        # Entraxe max sur x
        full_center_distance = self.reductor.full_center_distance()
        max_limit_x = self.limits['maximum']['x'] - full_center_distance
        if max_limit_x < 0:
            fonctionnelle += (max_limit_x*1e3)**2

        min_limit_x = full_center_distance - self.limits['minimum']['x']
        if min_limit_x < 0:
            fonctionnelle += (min_limit_x*1e3)**2

        # Diametres inférieurs à l'espace disponible
        for sa in self.reductor.shaft_assemblies:
            for gear in sa.gears:
                max_limit_y = self.limits['maximum']['y'] - gear.diameter
                if max_limit_y < 0:
                    fonctionnelle += (max_limit_y*1e3)**2
                min_limit_y = gear.diameter - self.limits['minimum']['y']
                if min_limit_y < 0:
                    fonctionnelle += (min_limit_y*1e3)**2

        # Contraintes accessoires
        for i_drive, drive in enumerate(self.reductor.drives):
            center_distance = drive.center_distance()
            r1 = self.reductor.shaft_assemblies[i_drive].accessory.diameter/2
            r2 = self.reductor.shaft_assemblies[i_drive+1].accessory.diameter/2
            accessory_distance = r2 + r1
            gap = center_distance - accessory_distance
            if gap < 0:
                fonctionnelle += (gap*1e3)**2
        return fonctionnelle

    def cond_init(self):
        x0=[]
        for interval in self.bounds:
            x0.append((interval[1]-interval[0])*float(npy.random.random(1))+interval[0])
        return x0

    def minimize(self, max_loops=1000):
        valid = True
        count = 0
        while valid and count < max_loops:
            x0 = self.cond_init()
            self.update(x0)
            res = minimize(self.objective, x0, bounds=self.bounds)
            count += 1
            if res.fun < 1e-8 and res.success:
                print(count)
                self.update(res.x)
                valid = False
                return res
            if count > max_loops:
                valid = False
                return res
        return res