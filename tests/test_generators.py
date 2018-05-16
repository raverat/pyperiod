import unittest

try:
    from unittest import mock
except:
    import mock

from datetime import date, datetime

from pyperiod import generators


class DailyGeneratorTestCase(unittest.TestCase):

    def setUp(self):
        self.patcher_datetime = mock.patch('pyperiod.generators.datetime',
                                           mock.Mock(wraps=datetime,
                                                     **{'now.return_value': datetime(2018, 1, 29, 8, 15, 1)}))
        self.patcher_datetime.start()

    def tearDown(self):
        self.patcher_datetime.stop()

    def test_default(self):
        from_datetime = datetime.combine(date(2018, 1, 30), datetime.min.time())
        to_datetime = datetime.combine(date(2018, 2, 5), datetime.max.time())

        gen = generators.Daily(from_datetime, to_datetime)

        self.assertListEqual(list(next(gen)), [datetime(2018, 1, 30, 0, 0, 0),
                                               datetime(2018, 1, 30, 23, 59, 59, 999999)])
        self.assertListEqual(list(next(gen)), [datetime(2018, 1, 31, 0, 0, 0),
                                               datetime(2018, 1, 31, 23, 59, 59, 999999)])

        self.assertListEqual(list(next(gen)), [datetime(2018, 2, 1, 0, 0, 0),
                                               datetime(2018, 2, 1, 23, 59, 59, 999999)])
        self.assertListEqual(list(next(gen)), [datetime(2018, 2, 2, 0, 0, 0),
                                               datetime(2018, 2, 2, 23, 59, 59, 999999)])
        self.assertListEqual(list(next(gen)), [datetime(2018, 2, 3, 0, 0, 0),
                                               datetime(2018, 2, 3, 23, 59, 59, 999999)])
        self.assertListEqual(list(next(gen)), [datetime(2018, 2, 4, 0, 0, 0),
                                               datetime(2018, 2, 4, 23, 59, 59, 999999)])
        self.assertListEqual(list(next(gen)), [datetime(2018, 2, 5, 0, 0, 0),
                                               datetime(2018, 2, 5, 23, 59, 59, 999999)])

        self.assertRaises(StopIteration, next, gen)

    def test_default_w_time(self):
        from_datetime = datetime(2018, 1, 30, 16, 7, 2)
        to_datetime = datetime(2018, 2, 5, 11, 4, 9)

        gen = generators.Daily(from_datetime, to_datetime)

        self.assertListEqual(list(next(gen)), [datetime(2018, 1, 30, 16, 7, 2),
                                               datetime(2018, 1, 30, 23, 59, 59, 999999)])
        self.assertListEqual(list(next(gen)), [datetime(2018, 1, 31, 0, 0, 0),
                                               datetime(2018, 1, 31, 23, 59, 59, 999999)])

        self.assertListEqual(list(next(gen)), [datetime(2018, 2, 1, 0, 0, 0),
                                               datetime(2018, 2, 1, 23, 59, 59, 999999)])
        self.assertListEqual(list(next(gen)), [datetime(2018, 2, 2, 0, 0, 0),
                                               datetime(2018, 2, 2, 23, 59, 59, 999999)])
        self.assertListEqual(list(next(gen)), [datetime(2018, 2, 3, 0, 0, 0),
                                               datetime(2018, 2, 3, 23, 59, 59, 999999)])
        self.assertListEqual(list(next(gen)), [datetime(2018, 2, 4, 0, 0, 0),
                                               datetime(2018, 2, 4, 23, 59, 59, 999999)])
        self.assertListEqual(list(next(gen)), [datetime(2018, 2, 5, 0, 0, 0),
                                               datetime(2018, 2, 5, 11, 4, 9)])

        self.assertRaises(StopIteration, next, gen)

    def test_shorter_than_period(self):
        from_datetime = datetime(2018, 1, 30, 4, 5, 6)
        to_datetime = datetime(2018, 1, 30, 16, 23, 56)

        gen = generators.Daily(from_datetime, to_datetime)

        self.assertListEqual(list(next(gen)), [datetime(2018, 1, 30, 4, 5, 6),
                                               datetime(2018, 1, 30, 16, 23, 56)])

        self.assertRaises(StopIteration, next, gen)

    def test_no_parameters(self):
        gen = generators.Daily()

        self.assertRaises(StopIteration, next, gen)

    def test_from_datetime_only__past(self):
        gen = generators.Daily(datetime(2018, 1, 27, 6, 9, 15))

        self.assertEqual(list(next(gen)), [datetime(2018, 1, 27, 6, 9, 15),
                                           datetime(2018, 1, 27, 23, 59, 59, 999999)])
        self.assertEqual(list(next(gen)), [datetime(2018, 1, 28),
                                           datetime(2018, 1, 28, 23, 59, 59, 999999)])

        self.assertEqual(list(next(gen)), [datetime(2018, 1, 29),
                                           datetime(2018, 1, 29, 8, 15, 1)])

        self.assertRaises(StopIteration, next, gen)

    def test_from_datetime_only__future(self):
        gen = generators.Daily(datetime(2018, 1, 31))

        self.assertRaises(StopIteration, next, gen)

    def test_to_datetime_only__past(self):
        gen = generators.Daily(to_datetime=datetime(2018, 1, 6, 11, 57, 3))

        self.assertRaises(StopIteration, next, gen)

    def test_to_datetime_only__future(self):
        gen = generators.Daily(to_datetime=datetime(2018, 2, 1, 2, 34, 45))

        self.assertEqual(list(next(gen)), [datetime(2018, 1, 29, 8, 15, 1),
                                           datetime(2018, 1, 29, 23, 59, 59, 999999)])
        self.assertEqual(list(next(gen)), [datetime(2018, 1, 30),
                                           datetime(2018, 1, 30, 23, 59, 59, 999999)])
        self.assertEqual(list(next(gen)), [datetime(2018, 1, 31),
                                           datetime(2018, 1, 31, 23, 59, 59, 999999)])
        self.assertEqual(list(next(gen)), [datetime(2018, 2, 1),
                                           datetime(2018, 2, 1, 2, 34, 45)])

        self.assertRaises(StopIteration, next, gen)


class WeeklyGeneratorTestCase(unittest.TestCase):

    def setUp(self):
        self.patcher_datetime = mock.patch('pyperiod.generators.datetime',
                                           mock.Mock(wraps=datetime,
                                                     **{'now.return_value': datetime(2018, 1, 29, 8, 15, 1)}))
        self.patcher_datetime.start()

    def tearDown(self):
        self.patcher_datetime.stop()

    def test_default(self):
        from_datetime = datetime.combine(date(2018, 1, 2), datetime.min.time())
        to_datetime = datetime.combine(date(2018, 1, 24), datetime.max.time())

        gen = generators.Weekly(from_datetime, to_datetime)

        self.assertListEqual(list(next(gen)), [datetime(2018, 1, 2),
                                               datetime(2018, 1, 7, 23, 59, 59, 999999)])
        self.assertListEqual(list(next(gen)), [datetime(2018, 1, 8),
                                               datetime(2018, 1, 14, 23, 59, 59, 999999)])
        self.assertListEqual(list(next(gen)), [datetime(2018, 1, 15),
                                               datetime(2018, 1, 21, 23, 59, 59, 999999)])
        self.assertListEqual(list(next(gen)), [datetime(2018, 1, 22),
                                               datetime(2018, 1, 24, 23, 59, 59, 999999)])

        self.assertRaises(StopIteration, next, gen)

    def test_default_w_time(self):
        from_datetime = datetime(2018, 1, 2, 16, 34, 2)
        to_datetime = datetime(2018, 1, 24, 7, 5, 24)

        gen = generators.Weekly(from_datetime, to_datetime)

        self.assertListEqual(list(next(gen)), [datetime(2018, 1, 2, 16, 34, 2),
                                               datetime(2018, 1, 7, 23, 59, 59, 999999)])
        self.assertListEqual(list(next(gen)), [datetime(2018, 1, 8),
                                               datetime(2018, 1, 14, 23, 59, 59, 999999)])
        self.assertListEqual(list(next(gen)), [datetime(2018, 1, 15),
                                               datetime(2018, 1, 21, 23, 59, 59, 999999)])
        self.assertListEqual(list(next(gen)), [datetime(2018, 1, 22),
                                               datetime(2018, 1, 24, 7, 5, 24)])

        self.assertRaises(StopIteration, next, gen)

    def test_shorter_than_period(self):
        from_datetime = datetime(2018, 1, 2, 16, 34, 2)
        to_datetime = datetime(2018, 1, 5, 23, 7, 45)

        gen = generators.Weekly(from_datetime, to_datetime)

        self.assertListEqual(list(next(gen)), [datetime(2018, 1, 2, 16, 34, 2),
                                               datetime(2018, 1, 5, 23, 7, 45)])

        self.assertRaises(StopIteration, next, gen)

    def test_no_parameters(self):
        gen = generators.Daily()

        self.assertRaises(StopIteration, next, gen)

    def test_from_datetime_only__past(self):
        gen = generators.Weekly(datetime(2018, 1, 16, 6, 9, 15))

        self.assertEqual(list(next(gen)), [datetime(2018, 1, 16, 6, 9, 15),
                                           datetime(2018, 1, 21, 23, 59, 59, 999999)])
        self.assertEqual(list(next(gen)), [datetime(2018, 1, 22),
                                           datetime(2018, 1, 28, 23, 59, 59, 999999)])

        self.assertEqual(list(next(gen)), [datetime(2018, 1, 29),
                                           datetime(2018, 1, 29, 8, 15, 1)])

        self.assertRaises(StopIteration, next, gen)

    def test_from_datetime_only__future(self):
        gen = generators.Weekly(datetime(2018, 1, 31))

        self.assertRaises(StopIteration, next, gen)

    def test_to_datetime_only__past(self):
        gen = generators.Weekly(to_datetime=datetime(2018, 1, 6, 11, 57, 3))

        self.assertRaises(StopIteration, next, gen)

    def test_to_datetime_only__future(self):
        gen = generators.Weekly(to_datetime=datetime(2018, 2, 16, 2, 34, 45))

        self.assertEqual(list(next(gen)), [datetime(2018, 1, 29, 8, 15, 1),
                                           datetime(2018, 2, 4, 23, 59, 59, 999999)])
        self.assertEqual(list(next(gen)), [datetime(2018, 2, 5),
                                           datetime(2018, 2, 11, 23, 59, 59, 999999)])
        self.assertEqual(list(next(gen)), [datetime(2018, 2, 12),
                                           datetime(2018, 2, 16, 2, 34, 45)])

        self.assertRaises(StopIteration, next, gen)


class MonthlyGeneratorTestCase(unittest.TestCase):

    def setUp(self):
        self.patcher_datetime = mock.patch('pyperiod.generators.datetime',
                                           mock.Mock(wraps=datetime,
                                                     **{'now.return_value': datetime(2018, 1, 29, 8, 15, 1)}))
        self.patcher_datetime.start()

    def tearDown(self):
        self.patcher_datetime.stop()

    def test_default(self):
        from_datetime = datetime.combine(date(2018, 1, 2), datetime.min.time())
        to_datetime = datetime.combine(date(2018, 4, 17), datetime.max.time())

        gen = generators.Monthly(from_datetime, to_datetime)

        self.assertListEqual(list(next(gen)), [datetime(2018, 1, 2),
                                               datetime(2018, 1, 31, 23, 59, 59, 999999)])
        self.assertListEqual(list(next(gen)), [datetime(2018, 2, 1),
                                               datetime(2018, 2, 28, 23, 59, 59, 999999)])
        self.assertListEqual(list(next(gen)), [datetime(2018, 3, 1),
                                               datetime(2018, 3, 31, 23, 59, 59, 999999)])
        self.assertListEqual(list(next(gen)), [datetime(2018, 4, 1),
                                               datetime(2018, 4, 17, 23, 59, 59, 999999)])

        self.assertRaises(StopIteration, next, gen)

    def test_default_w_time(self):
        from_datetime = datetime(2018, 1, 2, 16, 34, 2)
        to_datetime = datetime(2018, 4, 17, 7, 5, 24)

        gen = generators.Monthly(from_datetime, to_datetime)

        self.assertListEqual(list(next(gen)), [datetime(2018, 1, 2, 16, 34, 2),
                                               datetime(2018, 1, 31, 23, 59, 59, 999999)])
        self.assertListEqual(list(next(gen)), [datetime(2018, 2, 1),
                                               datetime(2018, 2, 28, 23, 59, 59, 999999)])
        self.assertListEqual(list(next(gen)), [datetime(2018, 3, 1),
                                               datetime(2018, 3, 31, 23, 59, 59, 999999)])
        self.assertListEqual(list(next(gen)), [datetime(2018, 4, 1),
                                               datetime(2018, 4, 17, 7, 5, 24)])

        self.assertRaises(StopIteration, next, gen)

    def test_shorter_than_period(self):
        from_datetime = datetime(2018, 1, 2, 16, 34, 2)
        to_datetime = datetime(2018, 1, 17, 23, 7, 45)

        gen = generators.Monthly(from_datetime, to_datetime)

        self.assertListEqual(list(next(gen)), [datetime(2018, 1, 2, 16, 34, 2),
                                               datetime(2018, 1, 17, 23, 7, 45)])

        self.assertRaises(StopIteration, next, gen)

    def test_no_parameters(self):
        gen = generators.Daily()

        self.assertRaises(StopIteration, next, gen)

    def test_from_datetime_only__past(self):
        gen = generators.Monthly(datetime(2017, 12, 23, 6, 9, 15))

        self.assertEqual(list(next(gen)), [datetime(2017, 12, 23, 6, 9, 15),
                                           datetime(2017, 12, 31, 23, 59, 59, 999999)])
        self.assertEqual(list(next(gen)), [datetime(2018, 1, 1),
                                           datetime(2018, 1, 29, 8, 15, 1)])

        self.assertRaises(StopIteration, next, gen)

    def test_from_datetime_only__future(self):
        gen = generators.Monthly(datetime(2018, 1, 31))

        self.assertRaises(StopIteration, next, gen)

    def test_to_datetime_only__past(self):
        gen = generators.Monthly(to_datetime=datetime(2018, 1, 6, 11, 57, 3))

        self.assertRaises(StopIteration, next, gen)

    def test_to_datetime_only__future(self):
        gen = generators.Monthly(to_datetime=datetime(2018, 4, 16, 2, 34, 45))

        self.assertEqual(list(next(gen)), [datetime(2018, 1, 29, 8, 15, 1),
                                           datetime(2018, 1, 31, 23, 59, 59, 999999)])
        self.assertEqual(list(next(gen)), [datetime(2018, 2, 1),
                                           datetime(2018, 2, 28, 23, 59, 59, 999999)])
        self.assertEqual(list(next(gen)), [datetime(2018, 3, 1),
                                           datetime(2018, 3, 31, 23, 59, 59, 999999)])
        self.assertEqual(list(next(gen)), [datetime(2018, 4, 1),
                                           datetime(2018, 4, 16, 2, 34, 45)])

        self.assertRaises(StopIteration, next, gen)
