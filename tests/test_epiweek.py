"""Unit tests for epiweek.py."""

# standard library
import unittest

# py3tester coverage target
__test_target__ = 'delphi.utils.epiweek'


class FunctionTests(unittest.TestCase):
  """Tests each function individually."""

  # past, present, and future
  sample_weeks = (
    # epiweek, year, and week
    (199740, 1997, 40),
    (201744, 2017, 44),
    (202727, 2027, 27),
  )

  # epiweek arithmetic samples
  sample_ranges = (
    # week1 + delta = week2
    (201744, 0, 201744),
    (201744, 1, 201745),
    (201744, -1, 201743),
    (201701, -1, 201652),
    (201501, -1, 201453),
    (199740, 1048, 201744),
    (202020, -1180, 199740),
  )

  def test_split_epiweek(self):
    for (ew, yr, wk) in BasicTests.sample_weeks:
      with self.subTest(ew=ew):
        a, b = split_epiweek(ew)
        self.assertEqual(yr, a)
        self.assertEqual(wk, b)

  def test_join_epiweek(self):
    for (ew, yr, wk) in BasicTests.sample_weeks:
      with self.subTest(ew=ew):
        x = join_epiweek(yr, wk)
        self.assertEqual(ew, x)

  def test_check_epiweek(self):
    for (ew, yr, wk) in BasicTests.sample_weeks:
      with self.subTest(ew=ew):
        self.assertTrue(check_epiweek(ew))
    with self.assertRaises(Exception):
      check_epiweek(201700)
    with self.assertRaises(Exception):
      check_epiweek(201753)
    self.assertFalse(check_epiweek(201753, fatal=False))

  def test_get_num_weeks(self):
    long_years = set([1997, 2003, 2008, 2014, 2020])
    for year in range(min(long_years) - 1, max(long_years) + 2):
      with self.subTest(year=year):
        num_weeks = 53 if year in long_years else 52
        self.assertEqual(get_num_weeks(year), num_weeks)

  def test_add_epiweeks(self):
    for ew1, delta, ew2 in BasicTests.sample_ranges:
      with self.subTest(ew1=ew1, delta=delta, ew2=ew2):
        self.assertEqual(add_epiweeks(ew1, delta), ew2)

  def test_get_season(self):
    for ew, y1, y2 in (
      (201744, 201740, 201820),
      (199740, 199740, 199820),
      (199820, 199740, 199820),
      (201453, 201440, 201520),
      (201430, None, None),
    ):
      with self.subTest(ew=ew, y1=y1, y2=y2):
        a, b = get_season(ew)
        self.assertEqual(a, y1)
        self.assertEqual(b, y2)

    # invalid epiweek
    with self.assertRaises(Exception):
      get_season(201553)

    # custom handler for offseason
    x, y = 'arbitrary', 'result'
    a, b = get_season(201730, lambda ew: (x, y))
    self.assertEqual(a, x)
    self.assertEqual(b, y)

  def test_delta_epiweeks(self):
    for ew1, delta, ew2 in BasicTests.sample_ranges:
      with self.subTest(ew1=ew1, delta=delta, ew2=ew2):
        self.assertEqual(delta_epiweeks(ew1, ew2), delta)

  def test_range_epiweeks(self):
    ew = 201744

    # need either start+stop or start+num
    with self.assertRaises(Exception):
      list(range_epiweeks(ew))

    # empty range...
    self.assertEqual(list(range_epiweeks(ew, stop=ew)), [])
    self.assertEqual(list(range_epiweeks(ew, num=0)), [])

    # ...unless inclusive...
    self.assertEqual(list(range_epiweeks(ew, stop=ew, inclusive=True)), [ew])

    # ...unless num=0
    self.assertEqual(list(range_epiweeks(ew, num=0, inclusive=True)), [])

    # works counting down explicitly...
    self.assertEqual(list(range_epiweeks(ew, num=-1)), [ew])

    # ...and implicitly
    ew1, ew2 = 201744, 201743
    actual = list(range_epiweeks(ew1, ew2, inclusive=True))
    self.assertEqual(actual, [ew1, ew2])

    # works across seasons, even on long years
    ew1, ew2 = 201552, 201301
    actual = list(range_epiweeks(ew1, ew2, inclusive=True))
    v1 = [i for i in range(201552, 201500, -1)]
    v2 = [i for i in range(201453, 201400, -1)]
    v3 = [i for i in range(201352, 201300, -1)]
    self.assertEqual(actual, v1 + v2 + v3)
