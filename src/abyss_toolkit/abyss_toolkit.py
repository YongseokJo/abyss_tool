import numpy as np
import yt
import importlib
import yt_utils
importlib.reload(yt_utils)
import yt_utils.particle_filters as pf
import yt_utils.utils as yu


class AbyssToolkit:
    def __init__(self):
        self.simulation_type = 'enzo-abyss' # or 'abyss'
        pass

    def loadAbyss(self, data_file):
        # Load Abyss data files
        pass
        self.simulation_type = 'abyss'
        return 

    def loadEnzo(self, path, snap_num, dir_name=None):
        # Load the data using yt
        self.path = path
        self.dir_name = dir_name

        yt.add_particle_filter("star", function=pf._star_filter, filtered_type='all', requires=["particle_type"])
        yt.add_particle_filter("all_star", function=pf._all_star_filter, filtered_type='all', requires=["particle_type"])
        yt.add_particle_filter("field_star", function=pf._field_star_filter, filtered_type='all', requires=["particle_type"])
        yt.add_particle_filter("DM", function=pf._dm_filter, filtered_type='all', requires=["particle_type"])
        yt.add_particle_filter("dark_matter", function=pf._true_dm_filter, filtered_type='all', requires=["particle_type"])
        yt.add_particle_filter("Nbody", function=pf._nbody_filter, filtered_type='all', requires=["particle_type"])
        yt.add_particle_filter("new_star", function=pf._new_star_filter, filtered_type='star', requires=["creation_time"])
        yt.add_particle_filter("young_star", function=pf._young_star_filter, filtered_type='all', requires=["creation_time"])

        if isinstance(snap_num, list) or isinstance(snap_num, np.ndarray) or isinstance(snap_num, range):
            self.ds = list()
            self.ad = list()
            for i in snap_num:
                a = yu.getEnzoPath(path, dir_name, i)
                print(a)
                self.ds.append(yt.load(yu.getEnzoPath(path, dir_name, i)))
                self.ad.append(self.ds[-1].all_data())
                try:
                    self.ds[-1].add_particle_filter("Nbody")
                    self.ds[-1].add_particle_filter("star")
                    self.ds[-1].add_particle_filter("DM")
                    self.ds[-1].add_particle_filter("dark_matter")
                    self.ds[-1].add_particle_filter("new_star")
                    self.ds[-1].add_particle_filter("all_star")
                    self.ds[-1].add_particle_filter("field_star")
                    self.ds[-1].add_particle_filter("young_star")
                    self.ds[-1].add_particle_filter("normal_star")
                except:
                    pass
        else:
            self.ds = yt.load(yu.getEnzoPath(path, dir_name, snap_num))
            self.ad = self.ds.all_data()
            try:
                self.ds.add_particle_filter("Nbody")
                self.ds.add_particle_filter("star")
                self.ds.add_particle_filter("DM")
                self.ds.add_particle_filter("dark_matter")
                self.ds.add_particle_filter("new_star")
                self.ds.add_particle_filter("all_star")
                self.ds.add_particle_filter("field_star")
                self.ds.add_particle_filter("young_star")
                self.ds.add_particle_filter("normal_star")
            except:
                pass
        self.simulation_type = 'enzo-abyss'
        return 



    def loadParticles(self, unit='cgs'):
        if unit == 'cgs':
            ulength = 'cm'
            umass = 'g'
            uvelocity = 'cm/s'


        if self.simulation_type == 'enzo-abyss':
            if isinstance(self.ds, list) or isinstance(self.ds, np.ndarray):
                data = list()
                for i in range(len(self.ds)):
                    pos = np.array(self.ad[i][("Nbody", "particle_position")])
                    pos = self.ds[i].arr(np.array(pos)-0.5, 'code_length')
                    pos = np.array(pos.in_units(ulength))
                    vel = np.array(
                        self.ad[i][("Nbody", "particle_velocity")].in_units(uvelocity))
                    mass = np.array(self.ad[i][("Nbody", "particle_mass")
                                        ].in_units(umass)).reshape(-1, 1)
                    data.append(np.c_[pos, vel, mass])
            else:
                pos = np.array(self.ad[("Nbody", "particle_position")])
                pos = self.ds.arr(np.array(pos)-0.5, 'code_length')
                pos = np.array(pos.in_units(ulength))
                vel = np.array(
                    self.ad[("Nbody", "particle_velocity")].in_units(uvelocity))
                mass = np.array(self.ad[("Nbody", "particle_mass")
                                    ].in_units(umass)).reshape(-1, 1)
                data = np.c_[pos, vel, mass]

        return data

    def saveParticles(self, data, snapnum, suffix=""):
        np.save("nbody_data/{}{:04}_nbody{}".format(self.dir_name,snapnum,suffix),data) 
