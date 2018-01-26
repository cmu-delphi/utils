"""Unit tests for populations.py."""

# standard library
import unittest

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
          self.assertTrue(get_population_weight(year, loc) >= 0)
