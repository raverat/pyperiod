import unittest

try:
    from unittest import mock
except:
    import mock

from datetime import datetime

from pyperiod import generators


class PropertyTestCase(unittest.TestCase):

    def setUp(self):
        self.patcher_datetime = mock.patch('pyperiod.generators.datetime',
                                           mock.Mock(wraps=datetime,
                                                     **{'now.return_value': datetime(2018, 1, 15, 13, 24, 7)}))
        self.patcher_datetime.start()

    def tearDown(self):
        self.patcher_datetime.stop()

    def test_default(self):
        gen = generators.BaseGenerator(datetime(2018, 1, 4, 15, 46, 8), datetime(2018, 4, 2, 7, 18, 3))

        self.assertEqual(gen.from_datetime, datetime(2018, 1, 4, 15, 46, 8))
        self.assertEqual(gen.to_datetime, datetime(2018, 4, 2, 7, 18, 3))

    def test_no_parameters(self):
        gen = generators.BaseGenerator()

        self.assertIsNone(gen.from_datetime)
        self.assertIsNone(gen.to_datetime)

    def test_from_datetime_only__past(self):
        gen = generators.BaseGenerator(datetime(2018, 1, 1))

        self.assertEqual(gen.from_datetime, datetime(2018, 1, 1))
        self.assertEqual(gen.to_datetime, datetime(2018, 1, 15, 13, 24, 7))

    def test_from_datetime_only__future(self):
        gen = generators.BaseGenerator(datetime(2018, 1, 31))

        self.assertEqual(gen.from_datetime, datetime(2018, 1, 31))
        self.assertIsNone(gen.to_datetime)

    def test_to_datetime_only__past(self):
        gen = generators.BaseGenerator(to_datetime=datetime(2018, 1, 6, 11, 57, 3))

        self.assertIsNone(gen.from_datetime)
        self.assertEqual(gen.to_datetime, datetime(2018, 1, 6, 11, 57, 3))

    def test_to_datetime_only__future(self):
        gen = generators.BaseGenerator(to_datetime=datetime(2018, 2, 6, 2, 34, 45))

        self.assertEqual(gen.from_datetime, datetime(2018, 1, 15, 13, 24, 7))
        self.assertEqual(gen.to_datetime, datetime(2018, 2, 6, 2, 34, 45))
