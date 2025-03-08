import numpy as np


def _all_star_filter(pfilter, data):
    return data[("all", "particle_mass")].in_units('Msun') < 3000


def _field_star_filter(pfilter, data):
    return np.logical_and(
        data[("all", "particle_mass")].in_units('Msun') < 3000,
        np.logical_or(
            data[("all", "particle_type")] == 1,
            data[("all", "particle_type")] == 2
        )
    )

def _star_filter(pfilter, data):
    return data[("all", "particle_type")] == 2


def _new_star_filter(pfilter, data):
    return data[("star", "creation_time")] > 0


def _dm_filter(pfilter, data):
    return data[("all", "particle_mass")].in_units('Msun') > 3000
    # return  data[("all", "particle_type")] == 1


def _true_dm_filter(pfilter, data):
    return data[("all", "particle_type")] == 1


def _nbody_filter(pfilter, data):
    return np.logical_or(data[("all", "particle_type")] == 101, data[("all", "particle_type")] == 12)


def _normal_filter(pfilter, data):
    return np.logical_or(
        np.logical_or(
            data[("all", "particle_type")] == 101,
            data[("all", "particle_type")] == 12
        ),
        np.logical_and(
            data[("all", "creation_time")] > 0,
            data[("all", "particle_type")] == 2
        )
    )


def _young_star_filter(pfilter, data):
    age = data.ds.current_time - \
        data[pfilter.filtered_type, "creation_time"]
    return age.in_units("Myr") <= 1.0


def _Star_filter(pfilter, data):
    return np.logical_or(np.logical_or(data[("all", "particle_type")] == 2,
                                        data[("all", "particle_type")] == 101),
                        data[("all", "particle_type")] == 11)
