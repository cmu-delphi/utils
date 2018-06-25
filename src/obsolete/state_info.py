"""
==================
=== Deprecated ===
==================

As of 2018-06-25, this file is no longer used. New code should use
geo/locations.py and geo/populations.py instead.


===============
=== Purpose ===
===============

Contains static data for US regions and states.


=================
=== Changelog ===
=================

2017-12-21
  - removed imputation (see impute_missing_values.py)
2016-11-15
  * use secrets
  * epidata API update
2016-04-06
  + initial version
"""


class StateInfo:

  def __init__(self):
    # names of all regions and states
    nat = ['nat']
    hhs = ['hhs%d' % r for r in range(1, 11)]
    cen = ['cen%d' % r for r in range(1, 10)]
    sta = [
      'AK', 'AL', 'AR', 'AZ', 'CA', 'CO', 'CT', 'DC',
      'DE', 'FL', 'GA', 'HI', 'IA', 'ID', 'IL', 'IN',
      'KS', 'KY', 'LA', 'MA', 'MD', 'ME', 'MI', 'MN',
      'MO', 'MS', 'MT', 'NC', 'ND', 'NE', 'NH', 'NJ',
      'NM', 'NV', 'NY', 'OH', 'OK', 'OR', 'PA', 'RI',
      'SC', 'SD', 'TN', 'TX', 'UT', 'VA', 'VT', 'WA',
      'WI', 'WV', 'WY'
    ]
    # population of each state
    population = {
      'AK':   731449, 'AL':  4822023, 'AR':  2949131, 'AZ':  6553255,
      'CA': 38041430, 'CO':  5187582, 'CT':  3590347, 'DC':   632323,
      'DE':   917092, 'FL': 19317568, 'GA':  9919945, 'HI':  1392313,
      'IA':  3074186, 'ID':  1595728, 'IL': 12875255, 'IN':  6537334,
      'KS':  2885905, 'KY':  4380415, 'LA':  4601893, 'MA':  6646144,
      'MD':  5884563, 'ME':  1329192, 'MI':  9883360, 'MN':  5379139,
      'MO':  6021988, 'MS':  2984926, 'MT':  1005141, 'NC':  9752073,
      'ND':   699628, 'NE':  1855525, 'NH':  1320718, 'NJ':  8864590,
      'NM':  2085538, 'NV':  2758931, 'NY': 19570261, 'OH': 11544225,
      'OK':  3814820, 'OR':  3899353, 'PA': 12763536, 'RI':  1050292,
      'SC':  4723723, 'SD':   833354, 'TN':  6456243, 'TX': 26059203,
      'UT':  2855287, 'VA':  8185867, 'VT':   626011, 'WA':  6897012,
      'WI':  5726398, 'WV':  1855413, 'WY':   576412,
    }
    # list of states in each region
    within = {
      'nat': sta,
      'hhs1': ['CT', 'MA', 'ME', 'NH', 'RI', 'VT'],
      'hhs2': ['NJ', 'NY'],
      'hhs3': ['DC', 'DE', 'MD', 'PA', 'VA', 'WV'],
      'hhs4': ['AL', 'FL', 'GA', 'KY', 'MS', 'NC', 'SC', 'TN'],
      'hhs5': ['IL', 'IN', 'MI', 'MN', 'OH', 'WI'],
      'hhs6': ['AR', 'LA', 'NM', 'OK', 'TX'],
      'hhs7': ['IA', 'KS', 'MO', 'NE'],
      'hhs8': ['CO', 'MT', 'ND', 'SD', 'UT', 'WY'],
      'hhs9': ['AZ', 'CA', 'HI', 'NV'],
      'hhs10': ['AK', 'ID', 'OR', 'WA'],
      'cen1': ['CT', 'MA', 'ME', 'NH', 'RI', 'VT'],
      'cen2': ['NJ', 'NY', 'PA'],
      'cen3': ['IL', 'IN', 'MI', 'OH', 'WI'],
      'cen4': ['IA', 'KS', 'MN', 'MO', 'ND', 'NE', 'SD'],
      'cen5': ['DC', 'DE', 'FL', 'GA', 'MD', 'NC', 'SC', 'VA', 'WV'],
      'cen6': ['AL', 'KY', 'MS', 'TN'],
      'cen7': ['AR', 'LA', 'OK', 'TX'],
      'cen8': ['AZ', 'CO', 'ID', 'MT', 'NM', 'NV', 'UT', 'WY'],
      'cen9': ['AK', 'CA', 'HI', 'OR', 'WA'],
    }
    for s in sta:
      within[s] = [s]
    # weight of each state in each region
    weight = {}
    for reg in nat + hhs + cen + sta:
      weight[reg] = {}
      states = within[reg]
      total = sum([population[s] for s in states])
      population[reg] = total
      for s in sta:
        if s in states:
          weight[reg][s] = population[s] / total
        else:
          weight[reg][s] = 0
    # the regions for each state
    state_regions = {}
    for s in sta:
      h, c = None, None
      for r in hhs:
        if s in within[r]:
          h = r
          break
      for r in cen:
        if s in within[r]:
          c = r
          break
      state_regions[s] = {'hhs': h, 'cen': c}
    # exports
    self.nat = nat
    self.hhs = hhs
    self.cen = cen
    self.sta = sta
    self.population = population
    self.within = within
    self.weight = weight
    self.state_regions = state_regions
