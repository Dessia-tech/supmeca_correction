#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 21:32:30 2019

@author: jezequel
"""
import matplotlib.pyplot as plt
from matplotlib import patches
import math

# =============================================================================

class Shaft:
    def __init__(self, position):
        self.position = position

    def plot(self, ax=None):
        if ax is None:
            _, ax = plt.subplots()
            ax.set_aspect('equal')
        pos_x, pos_y = self.position
        plt.plot(pos_x, pos_y, '*')

# =============================================================================

class Accessory:
    def __init__(self, diameter, length, speed, torque, name=''):
        self.diameter = diameter
        self.length = length
        self.speed = speed
        self.torque = torque
        self.name = name
        
    def volume(self):
        return self.diameter*math.pi*self.length

    def plot(self, position, ax=None):
        if ax is None:
            _, ax = plt.subplots()
            ax.set_aspect('equal')
        pos_x = position[0]
        pos_y = position[1]
        rayon = self.diameter/2.
        circle = patches.Circle((pos_x, pos_y), rayon, color='r', fill=False)
        ax.add_patch(circle)

# =============================================================================

class Drive:
    def __init__(self, gear1, gear2, name=''):
        self.gear1 = gear1
        self.gear2 = gear2
        self.gears = [gear1, gear2]

    def center_distance(self):
        center_distance = (self.gear1.diameter + self.gear2.diameter)/2
        return center_distance

    def ratio(self):
        ratio = self.gear1.diameter/self.gear2.diameter
        return ratio

    def gear_positions(self, pos_init=(0,0)):
        center_distance = self.center_distance()
        positions = {self.gear1 : pos_init,
                     self.gear2 : (pos_init[0] + center_distance, pos_init[1])}
        return positions
    
#    def update_gear2(self):
#        new_position = 
#        return 

    def output_speed(self, input_speed):
        ratio = self.ratio()
        output_speed = ratio*input_speed
        return output_speed

# =============================================================================

class Gear:
    def __init__(self, diameter, length, n_teeth=None, name=''):
        self.diameter = diameter
        self.length = length
        self.n_teeth = n_teeth
        self.name = name

    def module(self):
        module = self.diameter/self.n_teeth
        return module

    def step(self):
        module = self.module()
        step = math.pi*module
        return step
    
    def volume(self):
        return self.diameter*math.pi*self.length

    def plot(self, position, ax=None, stroke='k'):
        if ax is None:
            _, ax = plt.subplots()
            ax.set_aspect('equal')
        pos_x, pos_y = position
        circle = patches.Circle((pos_x, pos_y),
                                self.diameter/2.,
                                color=stroke,
                                fill=False)
        ax.add_patch(circle)

# =============================================================================

class ShaftAssembly:
    def __init__(self, shaft, gears, accessory=None, name=''):
        self.shaft = shaft
        self.gears = gears
        self.accessory = accessory
        self.name = name

    def plot(self, ax=None):
        if ax is None:
            _, ax = plt.subplots()
            ax.set_aspect('equal')
        self.shaft.plot(ax=ax)
        position = self.shaft.position
        if self.accessory is not None:
            self.accessory.plot(position, ax=ax)
        for gear in self.gears:
            gear.plot(position, ax=ax)

# =============================================================================

class Reductor:
    def __init__(self, shaft_assemblies, drives, name=''):
        self.shaft_assemblies = shaft_assemblies
        self.drives = drives
        self.name = name
        
#    def update(self):
#        for drive in self.drives:
#            drive.update_gear2
#        return 

    def plot(self, ax=None):
        if ax is None:
            fig, ax = plt.subplots()
            ax.set_aspect('equal')
            
        for shaft_assembly in self.shaft_assemblies:
            shaft_assembly.plot(ax=ax)
        ax.axis('scaled')

# =============================================================================