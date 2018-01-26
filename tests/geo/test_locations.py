"""Unit tests for locations.py."""

# standard library
import unittest

# py3tester coverage target
__test_target__ = 'delphi.utils.geo.locations'


class UnitTests(unittest.TestCase):
  """Basic unit tests."""

  def test_no_empty_regions(self):
    for loc in Locations.regions:
      with self.subTest(loc=loc):
        self.assertTrue(len(Locations.regions[loc]) > 0)
