"""
===============
=== Purpose ===
===============

Encodes the hierarchy of US political divisions.

This file, together with populations.py, replaces the static data portion of
state_info.py.

The location names used in this file match FluView names as specified in
fluview_locations.py of delphi-epidata.


===================
=== Explanation ===
===================

Although intended to be a more or less general-purpose description of the
various US geopolitical divisions, for all practical purposes the data in this
file corresponds to the FluView perspective of the world.

In this perspective, the US is a hierarchy where regions at any given level are
composed of smaller regions at a lower level. Notably, it may be possible to
subdivide a given region into multiple distinct sets of smaller regions.
However, the set of locations in any given subdivision fully covers and spans
the region being subdivided. In other words, there are never any gaps.

The root of the hierarchy is the national region (shortened to "nat") which
represents the entire US, including many of its territories. Each lower layer
of the hierarchy consists of smaller regions which combine together to form the
national region.

The leaves of the hierarchy are called "atoms" and have no further subdivisions
-- at least, not from a FluView perspective. These are typically US states,
although they also include some state fragments, territories, and cities.

By convention, the the middle layers of the hierarchy are collectively called
"regions". This includes, for example, the ten HHS regions as one subdivision
of national and the nine Census divisions as another. Each of the HHS and
Census regions is in turn made up of atoms -- mostly states, with a few
exceptions.
"""


class Locations:
  """Encodes the hierarchy of US political divisions."""

  # atomic regions for FluView data
  atom_list = [
    # entire states
    'ak', 'al', 'ar', 'az', 'ca', 'co', 'ct', 'de', 'fl', 'ga', 'hi', 'ia',
    'id', 'il', 'in', 'ks', 'ky', 'la', 'ma', 'md', 'me', 'mi', 'mn', 'mo',
    'ms', 'mt', 'nc', 'nd', 'ne', 'nh', 'nj', 'nm', 'nv', 'oh', 'ok', 'or',
    'pa', 'ri', 'sc', 'sd', 'tn', 'tx', 'ut', 'va', 'vt', 'wa', 'wi', 'wv',
    'wy',
    # state fragments
    'ny',
    # territories
    'dc', 'pr', 'vi',
    # cities
    'jfk',
  ]

  # national, HHS, and Census regions in terms of atoms
  nat = {
    'nat': atom_list,
  }
  hhs = {
    'hhs1': ['ct', 'ma', 'me', 'nh', 'ri', 'vt'],
    'hhs2': ['jfk', 'nj', 'ny', 'pr', 'vi'],
    'hhs3': ['dc', 'de', 'md', 'pa', 'va', 'wv'],
    'hhs4': ['al', 'fl', 'ga', 'ky', 'ms', 'nc', 'sc', 'tn'],
    'hhs5': ['il', 'in', 'mi', 'mn', 'oh', 'wi'],
    'hhs6': ['ar', 'la', 'nm', 'ok', 'tx'],
    'hhs7': ['ia', 'ks', 'mo', 'ne'],
    'hhs8': ['co', 'mt', 'nd', 'sd', 'ut', 'wy'],
    'hhs9': ['az', 'ca', 'hi', 'nv'],
    'hhs10': ['ak', 'id', 'or', 'wa'],
  }
  cen = {
    'cen1': ['ct', 'ma', 'me', 'nh', 'ri', 'vt'],
    'cen2': ['jfk', 'nj', 'ny', 'pa', 'pr', 'vi'],
    'cen3': ['il', 'in', 'mi', 'oh', 'wi'],
    'cen4': ['ia', 'ks', 'mn', 'mo', 'nd', 'ne', 'sd'],
    'cen5': ['dc', 'de', 'fl', 'ga', 'md', 'nc', 'sc', 'va', 'wv'],
    'cen6': ['al', 'ky', 'ms', 'tn'],
    'cen7': ['ar', 'la', 'ok', 'tx'],
    'cen8': ['az', 'co', 'id', 'mt', 'nm', 'nv', 'ut', 'wy'],
    'cen9': ['ak', 'ca', 'hi', 'or', 'wa'],
  }

  # atomic locations as regions containing only themselves
  atoms = {a: [a] for a in atom_list}

  # a single dictionary of all known locations
  regions = {}
  regions.update(nat)
  regions.update(hhs)
  regions.update(cen)
  regions.update(atoms)
