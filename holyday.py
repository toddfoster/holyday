import datetime
import sys
import argparse
import unittest

def main(argv=None):
    parser = argparse.ArgumentParser(description='Return information about the church calendar.')
    parser.add_argument('--date', nargs='?', type=datetime.date, default=datetime.date.today(), help='date in question')
    parser.add_argument('--test', action='store_true', help='Run unit tests')
    args = parser.parse_args()

    if args.test:
        sys.argv = sys.argv[:1]
        unittest.main()

    targetDate = args.date

    """
        HolyDay calculator.

        Every day is holy: a gift from God. But how do we mark them in the
        church? Enumeration and priority of feasts are based on the BCP,
        pp. 15ff. "The Calendar of the Church Year".
    """

    #TODO: decide input/output contents
    #   input = optional date + optional end date + parameters to define output
    #   output = plain text date, name of holy day, optionally requested additions, one per line
    #TODO: Calculate additional dates (and prioritize)
    #TODO: html interface
    #TODO: ical output
    #TODO: provide, but by default suppress, lesser feasts (commemorations)
    #TODO: Ember days
    #TODO: Rogration Days
    #TODO: provide (BCP) RCL readings on Sundays
    #TODO provide Daily Office readings
    #TODO: provide collects for Sundays, principal feasts

    #TODO: rm example testing output
    easter = calc_easter(targetDate.year)
    advent = calc_advent(targetDate.year)
    print "Easter = " + easter.isoformat()
    print "Advent = " + advent.isoformat()


def calc_advent(year):
    christmas = datetime.date(year,12,25)
    # Back up four weeks from Christmas,
    # thus skipping over all four Sundays of Advent
    advent = christmas - datetime.timedelta(weeks=4)
    # If not a Sunday, move forward to Sunday
    if (advent.weekday() < 6):
        advent = advent + datetime.timedelta(days=(6 - advent.weekday()))
    return advent


def calc_easter(year):
    """
    Returns Easter as a date object.

    An implementation of Butcher's Algorithm for determining the date of
    Easter for the Western church. Works for any date in the Gregorian
    calendar (1583 and onward). Returns a date object.

    From:
    http://code.activestate.com/recipes/576517-calculate-easter-western-given-a-year/
    """
    a = year % 19
    b = year // 100
    c = year % 100
    d = (19 * a + b - b // 4 - ((b - (b + 8) // 25 + 1) // 3) + 15) % 30
    e = (32 + 2 * (b % 4) + 2 * (c // 4) - d - (c % 4)) % 7
    f = d + e - 7 * ((a + 11 * d + 22 * e) // 451) + 114
    month = f // 31
    day = f % 31 + 1
    return datetime.date(year, month, day)


class testDateManipulation(unittest.TestCase):
    # Quick tutorial on Unittest: http://pymbook.readthedocs.org/en/latest/testing.html
    # Helpful chart of dates to test: http://www.infoplease.com/ipa/A0113948.html
    def test_easter(self):
        self.assertEqual(datetime.date(2000,04,23), calc_easter(2000))
        self.assertEqual(datetime.date(2001,04,15), calc_easter(2001))
        self.assertEqual(datetime.date(2006,04,16), calc_easter(2006))
        self.assertEqual(datetime.date(2011,04,24), calc_easter(2011))
        self.assertEqual(datetime.date(2016,03,27), calc_easter(2016))
        self.assertEqual(datetime.date(2096,04,15), calc_easter(2096))

    def test_advent(self):
        self.assertEqual(datetime.date(2000,12,03), calc_advent(2000))
        self.assertEqual(datetime.date(2001,12,02), calc_advent(2001))
        self.assertEqual(datetime.date(2005,11,27), calc_advent(2005))
        self.assertEqual(datetime.date(2010,11,28), calc_advent(2010))
        self.assertEqual(datetime.date(2015,11,29), calc_advent(2015))


if __name__ == "__main__":
    sys.exit(main())
