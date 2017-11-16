"""Unit tests for epidate.py."""

# standard library
import unittest

# first party
import delphi.utils.epiweek as utils_epiweek

# py3tester coverage target
__test_target__ = 'delphi.utils.epidate'


class FunctionTests(unittest.TestCase):
  """Tests each function individually."""

  # year, month, day, epi-year, epi-week
  sample_epiweeks = (
    (2006, 12, 30, 2006, 52),
    (2006, 12, 31, 2007, 1),
    (2009, 1, 3, 2008, 53),
    (2009, 1, 4, 2009, 1),
    (2015, 1, 3, 2014, 53),
    (2015, 1, 4, 2015, 1),
    (2016, 12, 31, 2016, 52),
    (2017, 1, 1, 2017, 1),
    (2017, 11, 14, 2017, 46),
    (2017, 12, 30, 2017, 52),
    (2017, 12, 31, 2018, 1),
  )

  def assert_date(self, date, y, m, d):
    """Assert that year, month, and day components are equal."""
    self.assertEqual(date.get_year(), y)
    self.assertEqual(date.get_month(), m)
    self.assertEqual(date.get_day(), d)

  def test_constructor(self):
    # valid dates
    for year, month, day in (
      (2017, 11, 14),
      (2017, 2, 28),
      (2016, 2, 29),
      (1, 1, 1),
      (9999, 12, 31),
    ):
      with self.subTest(year=year, month=month, day=day):
        date = EpiDate(year, month, day)
        self.assertEqual(date.get_year(), year)
        self.assertEqual(date.get_month(), month)
        self.assertEqual(date.get_day(), day)

    # invalid dates
    for year, month, day in (
      (0, 11, 14),
      (2017, 0, 14),
      (2017, 13, 14),
      (2017, 11, 0),
      (2017, 11, 31),
      (2017, 2, 29),
      (2016, 2, 30),
    ):
      with self.subTest(year=year, month=month, day=day):
        with self.assertRaises(Exception):
          EpiDate(year, month, day)

  def test_is_leap_year(self):
    leaps = (1600, 2000, 2004, 2008, 2012, 2016, 2400)
    for i, year in enumerate(leaps):
      # shouldn't matter what month or day is (as long as it's valid)
      month = (3 * i) % 12 + 1
      day = (7 * i) % 28 + 1
      with self.subTest(year=year):
        self.assertTrue(EpiDate(year, month, day).is_leap_year())
      # the next 3 years must be common
      for i in range(3):
        year += 1
        with self.subTest(year=year):
          self.assertFalse(EpiDate(year, month, day).is_leap_year())

  def test_get_index(self):
    # helper to get the index from a date
    idx = lambda y, m, d: EpiDate(y, m, d).get_index()

    # indices are sequential
    a = idx(2017, 1, 1)
    b = idx(2017, 1, 2)
    c = idx(2017, 1, 3)
    self.assertEqual(a + 1, b)
    self.assertEqual(b + 1, c)

    # indices respect leap years
    a = idx(2004, 1, 1)
    b = idx(2005, 1, 1)
    c = idx(2006, 1, 1)
    self.assertEqual(b - a, 366)
    self.assertEqual(c - b, 365)
    a = idx(800, 1, 1)
    b = idx(2000, 1, 1)
    c = idx(3200, 1, 1)
    self.assertEqual(b - a, c - b)

  def test_get_day_of_week(self):
    # helper to get the week day from a date
    day = lambda y, m, d: EpiDate(y, m, d).get_day_of_week()

    # known week days, Sunday through Saturday
    self.assertEqual(day(2345, 12, 2), 0)
    self.assertEqual(day(1867, 7, 1), 1)
    self.assertEqual(day(2017, 11, 14), 2)
    self.assertEqual(day(2017, 5, 3), 3)
    self.assertEqual(day(1776, 7, 4), 4)
    self.assertEqual(day(2017, 5, 5), 5)
    self.assertEqual(day(2017, 5, 6), 6)

  def test_get_ew_year(self):
    for y, m, d, ey, ew in FunctionTests.sample_epiweeks:
      with self.subTest(y=y, m=m, d=d, ey=ey):
        self.assertEqual(EpiDate(y, m, d).get_ew_year(), ey)

  def test_get_ew_week(self):
    for y, m, d, ey, ew in FunctionTests.sample_epiweeks:
      with self.subTest(y=y, m=m, d=d, ew=ew):
        self.assertEqual(EpiDate(y, m, d).get_ew_week(), ew)

  def test_get_ew(self):
    for y, m, d, ey, ew in FunctionTests.sample_epiweeks:
      epwk = utils_epiweek.join_epiweek(ey, ew)
      with self.subTest(y=y, m=m, d=d, epwk=epwk):
        self.assertEqual(EpiDate(y, m, d).get_ew(), epwk)

  def test_add_days(self):
    date = EpiDate(2017, 11, 14)

    # trivial examples
    self.assert_date(date.add_days(0), 2017, 11, 14)
    self.assert_date(date.add_days(1), 2017, 11, 15)
    self.assert_date(date.add_days(7), 2017, 11, 21)
    self.assert_date(date.add_days(365), 2018, 11, 14)
    self.assert_date(date.add_days(-365), 2016, 11, 14)

    # there are 146097 days in any given 400 year period
    self.assert_date(date.add_days(146097), 2417, 11, 14)
    self.assert_date(date.add_days(-146097), 1617, 11, 14)

  def test_add_weeks(self):
    date = EpiDate(2017, 11, 14)

    # simple examples
    self.assert_date(date.add_weeks(0), 2017, 11, 14)
    self.assert_date(date.add_weeks(1), 2017, 11, 21)

    # index-based examples
    idx = date.get_index()
    for weeks in (0, 1, 10, 100, -100):
      with self.subTest(weeks=weeks):
        self.assertEquals(date.add_weeks(weeks).get_index(), idx + weeks * 7)

  def test_add_months(self):
    # simple examples
    date = EpiDate(2017, 11, 14)
    self.assert_date(date.add_months(0), 2017, 11, 14)
    self.assert_date(date.add_months(1), 2017, 12, 14)
    self.assert_date(date.add_months(2), 2018, 1, 14)
    self.assert_date(date.add_months(12), 2018, 11, 14)
    self.assert_date(date.add_months(48), 2021, 11, 14)
    self.assert_date(date.add_months(-96), 2009, 11, 14)

    # edge cases
    date = EpiDate(2016, 2, 29)
    self.assert_date(date.add_months(0), 2016, 2, 29)
    self.assert_date(date.add_months(1), 2016, 3, 29)
    self.assert_date(date.add_months(2), 2016, 4, 29)
    self.assert_date(date.add_months(12), 2017, 2, 28)
    self.assert_date(date.add_months(48), 2020, 2, 29)
    self.assert_date(date.add_months(-96), 2008, 2, 29)
    self.assert_date(EpiDate(2016, 3, 30).add_months(-1), 2016, 2, 29)
    self.assert_date(EpiDate(2017, 3, 30).add_months(-1), 2017, 2, 28)
    date = EpiDate(2017, 1, 31)
    self.assert_date(date.add_months(-2), 2016, 11, 30)
    self.assert_date(date.add_months(-11), 2016, 2, 29)
    self.assert_date(date.add_months(-23), 2015, 2, 28)

  def test_add_years(self):
    # simple examples
    date = EpiDate(2017, 11, 14)
    self.assert_date(date.add_years(0), 2017, 11, 14)
    self.assert_date(date.add_years(1), 2018, 11, 14)
    self.assert_date(date.add_years(-10), 2007, 11, 14)

    # edge cases
    date = EpiDate(2016, 2, 29)
    self.assert_date(date.add_years(-1), 2015, 2, 28)
    self.assert_date(date.add_years(-816), 1200, 2, 29)
    self.assert_date(EpiDate(2003, 2, 28).add_years(1), 2004, 2, 28)

  def test_str(self):
    s = str(EpiDate(2017, 3, 4))
    self.assertIn('2017', s)
    self.assertIn('03', s)
    self.assertIn('04', s)
    self.assertEqual(len(s), 10)

  def test_get_day_name(self):
    self.assertEqual(EpiDate.get_day_name(0).lower(), 'sunday')
    self.assertEqual(EpiDate.get_day_name(0, short=True).lower(), 'sun')
    self.assertEqual(EpiDate.get_day_name(1).lower(), 'monday')
    self.assertEqual(EpiDate.get_day_name(1, short=True).lower(), 'mon')
    self.assertEqual(EpiDate.get_day_name(6).lower(), 'saturday')
    self.assertEqual(EpiDate.get_day_name(6, short=True).lower(), 'sat')

  def test_get_month_name(self):
    self.assertEqual(EpiDate.get_month_name(1).lower(), 'january')
    self.assertEqual(EpiDate.get_month_name(1, short=True).lower(), 'jan')
    self.assertEqual(EpiDate.get_month_name(2).lower(), 'february')
    self.assertEqual(EpiDate.get_month_name(2, short=True).lower(), 'feb')
    self.assertEqual(EpiDate.get_month_name(12).lower(), 'december')
    self.assertEqual(EpiDate.get_month_name(12, short=True).lower(), 'dec')

  def test_today(self):
    self.assertIsNotNone(EpiDate.today())

  def test_from_string(self):
    strs = ['2017-01-01', '2017/01/01', '2017@01$01', '2017901101', '20170101']
    for s in strs:
      with self.subTest(s=s):
        self.assert_date(EpiDate.from_string(s), 2017, 1, 1)
    with self.assertRaises(Exception):
      EpiDate.from_string('this is not a date string')

  def test_from_index(self):
    date1 = EpiDate(2017, 11, 14)
    idx = date1.get_index()
    date2 = EpiDate.from_index(idx)
    y, m, d = date1.get_year(), date1.get_month(), date1.get_day()
    self.assert_date(date2, y, m, d)

    first_index = EpiDate(1800, 1, 1).get_index()
    last_index = EpiDate(2200, 12, 31).get_index()
    for idx in range(first_index, last_index + 1):
      self.assertEqual(EpiDate.from_index(idx).get_index(), idx)

    with self.assertRaises(Exception):
      EpiDate.from_index(-1)

  def test_from_epiweek(self):
    for y, m, d, ey, ew in FunctionTests.sample_epiweeks:
      epwk = utils_epiweek.join_epiweek(ey, ew)
      with self.subTest(y=y, m=m, d=d, epwk=epwk):
        date1 = EpiDate(y, m, d)
        date2 = EpiDate.from_epiweek(ey, ew)
        self.assertEqual(date1.get_ew(), epwk)
        self.assertEqual(date2.get_ew(), epwk)
        self.assertEqual(date2.get_day_of_week(), 3)

    for year in range(2000, 2020):
      for week in range(1, utils_epiweek.get_num_weeks(year) + 1):
        epwk = utils_epiweek.join_epiweek(year, week)
        date = EpiDate.from_epiweek(year, week)
        self.assertEqual(date.get_ew(), epwk)
        self.assertEqual(date.get_day_of_week(), 3)

    with self.assertRaises(Exception):
      EpiDate.from_epiweek(2017, 0)
    with self.assertRaises(Exception):
      EpiDate.from_epiweek(2017, 53)
    with self.assertRaises(Exception):
      EpiDate.from_epiweek(0, 30)
