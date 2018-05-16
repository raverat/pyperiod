import calendar

from datetime import datetime, timedelta


class BaseGenerator(object):

    start = None
    end = None

    delta = None

    def __init__(self, from_datetime=None, to_datetime=None):
        self._from_datetime = from_datetime
        self._to_datetime = to_datetime

        if self._from_datetime is None and self._to_datetime and self._to_datetime > datetime.now():
            self._from_datetime = datetime.now()

        if self._to_datetime is None and self._from_datetime and self._from_datetime < datetime.now():
            self._to_datetime = datetime.now()

    @property
    def from_datetime(self):
        return self._from_datetime

    @property
    def to_datetime(self):
        return self._to_datetime

    def __iter__(self):
        return self

    def __next__(self):
        return self.next()

    def next(self):
        raise NotImplemented

    def to_list(self):
        return list(self)


class Daily(BaseGenerator):

    delta = timedelta(days=1)

    def next(self):
        if not self.from_datetime or not self.to_datetime:
            raise StopIteration

        if not self.start:
            self.start = self.from_datetime
        else:
            self.start = datetime.combine((self.start + self.delta).date(), datetime.min.time())

        if self.start > self.to_datetime:
            raise StopIteration

        self.end = datetime.combine(self.start.date(), datetime.max.time())

        return self.start, min(self.to_datetime, self.end)


class Weekly(BaseGenerator):

    def next(self):
        if not self.from_datetime or not self.to_datetime:
            raise StopIteration

        if not self.start:
            self.start = self.from_datetime
            self.end = datetime.combine((self.start + timedelta(days=6 - self.start.weekday())).date(),
                                        datetime.max.time())
        else:
            self.start = datetime.combine((self.end + timedelta(days=1)).date(),
                                          datetime.min.time())
            self.end = datetime.combine((self.start + timedelta(days=6)).date(),
                                        datetime.max.time())

        if self.start > self.to_datetime:
            raise StopIteration

        return self.start, min(self.to_datetime, self.end)


class Monthly(BaseGenerator):

    def next(self):
        if not self.from_datetime or not self.to_datetime:
            raise StopIteration

        if not self.start:
            self.start = self.from_datetime
        else:
            self.start = datetime.combine((self.end + timedelta(days=1)).date(),
                                          datetime.min.time())

        if self.start > self.to_datetime:
            raise StopIteration

        weekday, nb_of_days = calendar.monthrange(self.start.year, self.start.month)
        self.end = datetime.combine(self.start.replace(day=nb_of_days).date(),
                                    datetime.max.time())

        return self.start, min(self.to_datetime, self.end)
