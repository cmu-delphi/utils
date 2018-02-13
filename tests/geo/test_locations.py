"""Unit tests for locations.py."""

# standard library
import unittest

# py3tester coverage target
__test_target__ = 'delphi.utils.geo.locations'


class UnitTests(unittest.TestCase):
  """Basic unit tests."""

  def test_no_empty_regions(self):
    for loc in Locations.region_map:
      with self.subTest(loc=loc):
        self.assertTrue(len(Locations.region_map[loc]) > 0)

  def test_consistent_regions(self):
    self.assertEqual(set(Locations.region_list), Locations.region_map.keys())

  def test_expected_regions(self):
    expected = set([
      'nat', 'hhs1', 'hhs10', 'cen1', 'cen9', 'pa', 'ca', 'dc', 'pr', 'jfk'
    ])
    self.assertTrue(set(Locations.region_list) > expected)

  def test_lower_case_names(self):
    for name in Locations.region_list:
      self.assertEqual(name, name.lower())
