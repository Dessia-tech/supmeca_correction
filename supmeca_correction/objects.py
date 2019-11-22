#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 21:32:30 2019

@author: jezequel
"""
import matplotlib.pyplot as plt
from matplotlib import patches
import math
import volmdlr as vm
import volmdlr.primitives3D as p3d
import volmdlr.primitives2D as p2d

# =============================================================================

class Shaft:
    def __init__(self, pos_x, pos_y):
        self.pos_x = pos_x
        self.pos_y = pos_y

    def plot(self, ax=None):
        if ax is None:
            _, ax = plt.subplots()
            ax.set_aspect('equal')
        plt.plot(self.pos_x, self.pos_y, '*')

    def babylon(self, length, z_position):
        primitives = []
        pos = vm.Point3D((self.pos_x, self.pos_y, z_position))
        axis = vm.Vector3D((0,0,1))
        radius = 0.02
        cylinder = p3d.Cylinder(pos, axis, radius, length)
        primitives.append(cylinder)
        return primitives

# =============================================================================

class Accessory:
    def __init__(self, diameter, length, speed, torque=0, name=''):
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

    def babylon(self, xy_position, z_position):
        primitives = []
        pos = vm.Point3D((xy_position[0], xy_position[1], z_position))
        axis = vm.Vector3D((0,0,1))
        radius = self.diameter/2
        length = self.length
        cylinder = p3d.Cylinder(pos, axis, radius, length)
        primitives.append(cylinder)
        return primitives

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

    def babylon(self, xy_position, z_position):
        primitives = []

        ## AFFICHAGE EN CYLINDRE ##
#        pos = vm.Point3D((xy_position[0], xy_position[1], z_position))
#        axis = vm.Vector3D((0,0,1))
#        radius = self.diameter/2
#        length = self.length
#        cylinder = p3d.Cylinder(pos, axis, radius, length)
#        primitives.append(cylinder)

        ## AFFICHAGE EN ROUE DENTEE ##
        plane_origin = vm.Point3D((xy_position[0], xy_position[1], z_position-self.length/2))
        x = vm.x3D
        y = vm.y3D
        vector = vm.Vector3D((0,0,self.length))

        if self.n_teeth is None:
            n_teeth = int(round(self.diameter*100, 0))
        else:
            n_teeth = self.n_teeth
        angle = 2*math.pi/n_teeth
        inner_diameter = 0.90 * self.diameter
        teeth_l = (2*math.pi*self.diameter/2) / (1.5*n_teeth)
        pt1 = vm.Point2D((-teeth_l/2, (inner_diameter**2 / 4 - teeth_l**2 / 4)**0.5))
        pt5 = vm.Point2D(( teeth_l/2, (inner_diameter**2 / 4 - teeth_l**2 / 4)**0.5))
        pt2 = vm.Point2D((pt1.vector[0]/2, self.diameter/2))
        pt4 = vm.Point2D((pt5.vector[0]/2, self.diameter/2))
        rls_points = [pt1, pt2, pt4, pt5]
        for i in range(n_teeth-1):
            new_pt1 = rls_points[-4].Rotation(vm.o2D, -angle)
            new_pt2 = rls_points[-3].Rotation(vm.o2D, -angle)
            new_pt4 = rls_points[-2].Rotation(vm.o2D, -angle)
            new_pt5 = rls_points[-1].Rotation(vm.o2D, -angle)
            rls_points.extend([new_pt1, new_pt2, new_pt4, new_pt5])

        rls_points.reverse()
        rls = p2d.RoundedLineSegments2D(rls_points, {}, True)
        outer_contour2d = vm.Contour2D([rls])
        extrusion = p3d.ExtrudedProfile(plane_origin, x, y, outer_contour2d, [], vector)
        primitives.append(extrusion)
        return primitives

# =============================================================================

class ShaftAssembly:
    def __init__(self, shaft, gears, accessory=None, offset=0.05, name=''):
        self.offset = offset
        self.shaft = shaft
        self.gears = gears
        self.accessory = accessory
        self.name = name

        self.pos_z = 0

    def shaft_length(self):
        """
        Calcule la longueur de l'arbre pour l'affichage Babylon
        """
        if self.accessory is not None:
            length = 2*self.offset + self.accessory.length
        else:
            length = self.offset
        for gear in self.gears:
            length += gear.length
            length += self.offset
        return length

    def position_along_z(self):
        """
        Renvoie un dictionnaire avec la position selon z de l'accessoire et des shafts
        """
        z_positions_dict = {}
        z_sweeper = self.pos_z + self.offset
        if self.accessory is not None:
            z_positions_dict[self.accessory] = z_sweeper + self.accessory.length/2
            z_sweeper += self.accessory.length + self.offset
        for gear in self.gears:
            z_positions_dict[gear] = z_sweeper + gear.length/2
            z_sweeper += gear.length + self.offset
        return z_positions_dict

    def plot(self, ax=None):
        if ax is None:
            _, ax = plt.subplots()
            ax.set_aspect('equal')
        self.shaft.plot(ax=ax)
        position = (self.shaft.pos_x, self.shaft.pos_y)
        if self.accessory is not None:
            self.accessory.plot(position, ax=ax)
        for gear in self.gears:
            gear.plot(position, ax=ax)

    def babylon(self):
        z_positions_dict = self.position_along_z()
        xy_position = self.shaft.position
        primitives = []
        shaft_length = self.shaft_length()

        primitives.extend(self.shaft.babylon(shaft_length, self.pos_z + shaft_length/2))

        for gear in self.gears:
            primitives.extend(gear.babylon(xy_position, z_positions_dict[gear]))

        if self.accessory is not None:
            primitives.extend(self.accessory.babylon(xy_position, z_positions_dict[self.accessory]))

        return primitives

# =============================================================================

class Reductor:
    def __init__(self, shaft_assemblies, drives, name=''):
        self.shaft_assemblies = shaft_assemblies
        self.drives = drives
        self.name = name

        self.check()
        self.link_shaft_assemblies()

    def speeds(self):
        ref_accessory = self.shaft_assemblies[0].accessory
        input_speed = ref_accessory.speed

        speeds = [input_speed]
        for drive in self.drives:
            output_speed = drive.output_speed(input_speed)
            speeds.append(output_speed)
            input_speed = output_speed
        return speeds

    def update(self, x):
        gears = [gear for sa in self.shaft_assemblies for gear in sa.gears]

        for gear_diameter, gear in zip(x, gears):
            gear.diameter = gear_diameter

        self.link_shaft_assemblies()

    def full_center_distance(self):
        first_shaft = self.shaft_assemblies[0].shaft
        last_shaft = self.shaft_assemblies[-1].shaft

        return last_shaft.pos_x - first_shaft.pos_x

    def check(self):
        if len(self.drives)+1 != len(self.shaft_assemblies):
            raise Exception("Le nombre de shaft_assemblies et le nombre de drives \
                            ne correspondent pas")

        for i, (shaft_assembly1, shaft_assembly2) in enumerate(tuple(zip(self.shaft_assemblies[:-1], self.shaft_assemblies[1:]))):
            if self.drives[i].gear1 not in shaft_assembly1.gears:
                raise Exception("L'attribut drives ne correspond pas à l'ordre \
                                indiqué par l'attribut shaft_assemblies")
            if self.drives[i].gear2 not in shaft_assembly2.gears:
                raise Exception("L'attribut drives ne correspond pas à l'ordre \
                                indiqué par l'attribut shaft_assemblies")

    def link_shaft_assemblies(self):
        for i, (shaft_assembly1, shaft_assembly2) in enumerate(tuple(zip(self.shaft_assemblies[:-1], self.shaft_assemblies[1:]))):
            drive = self.drives[i]

            position_dict = drive.gear_positions((shaft_assembly1.shaft.pos_x,
                                                  shaft_assembly1.shaft.pos_y))
            new_position = position_dict[drive.gear2]
            shaft_assembly2.shaft.pos_x = new_position[0]
            shaft_assembly2.shaft.pos_y = new_position[1]

            z_position_dict1 = shaft_assembly1.position_along_z()
            z_position_dict2 = shaft_assembly2.position_along_z()
            gear1_pos_z = z_position_dict1[drive.gear1]
            gear2_pos_z = z_position_dict2[drive.gear2]
            shaft_assembly2.pos_z = gear1_pos_z - gear2_pos_z

    def plot(self, ax=None):
        if ax is None:
            fig, ax = plt.subplots()
            ax.set_aspect('equal')

        for shaft_assembly in self.shaft_assemblies:
            shaft_assembly.plot(ax=ax)
        ax.axis('scaled')

    def babylon(self):
        primitives = []
        for shaft_assembly in self.shaft_assemblies:
            primitives.extend(shaft_assembly.babylon())
        volumemodel = vm.VolumeModel(primitives, name=self.name)
        volumemodel.BabylonShow()
        return primitives

# =============================================================================