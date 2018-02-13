"""Unit tests for populations.py."""

# standard library
import unittest

# first party
from delphi.utils.geo.locations import Locations

# py3tester coverage target
__test_target__ = 'delphi.utils.geo.populations'


class UnitTests(unittest.TestCase):
  """Basic unit tests."""

  def test_weights_sum_to_one(self):
    for year in population_weights:
      with self.subTest(year=year):
        total = sum(population_weights[year].values())
        self.assertEqual(round(total, 5), 1)

  def test_weights_are_nonnegative(self):
    for year in population_weights:
      for loc in population_weights[year]:
        with self.subTest(year=year, loc=loc):
          self.assertTrue(get_population_weight(loc, year) >= 0)

  def test_locations_are_atoms(self):
    for year in population_weights:
      for loc in population_weights[year]:
        with self.subTest(year=year, loc=loc):
          self.assertIn(loc, Locations.atom_list)

  def test_season_defaults_to_latest(self):
    location = 'sd'
    season = max(population_weights)
    val1 = get_population_weight(location, season)
    val2 = get_population_weight(location)
    self.assertEqual(val1, val2)

  def test_population_is_integer(self):
    pop = get_population('vi')
    self.assertTrue(isinstance(pop, int))
