import decimal
import random

from datetime import datetime
from dateutil import tz

from surety.sdk import fakeable, dates
from surety.sdk.base_enum import BaseEnum
from surety.sdk.field import Field
from surety.process import dictionary


class Bool(Field):
    def generate_value(self):
        return fakeable.FAKER.boolean()


class Int(Field):
    def __init__(self, name=None, required=True, allow_none=False,
                 min_val=None, max_val=None, default=None):
        self.save_kwargs(locals())
        self.min_val = min_val or 0
        self.max_val = max_val or 9999
        super().__init__(
            name=name, required=required, allow_none=allow_none,
            default=default
        )

    def generate_value(self):
        return fakeable.FAKER.pyint(
            min_value=self.min_val,
            max_value=self.max_val
        )


class Float(Field):
    def __init__(self, name=None, required=True, allow_none=False, i_len=None,
                 f_len=None, min_val=None, max_val=None, positive=None,
                 default=None):
        self.save_kwargs(locals())
        self.i_len = i_len
        self.f_len = f_len
        self.min_val = min_val
        self.max_val = max_val
        self.positive = positive
        super().__init__(
            name=name, required=required, allow_none=allow_none,
            default=default
        )

    def generate_value(self):
        return fakeable.FAKER.pyfloat(
            left_digits=self.i_len,
            right_digits=self.f_len,
            positive=bool(self.positive),
            min_value=self.min_val,
            max_value=self.max_val
        )


class Decimal(Float):
    def generate_value(self):
        return fakeable.FAKER.pydecimal(
            left_digits=self.i_len or 1,
            right_digits=self.f_len,
            positive=self.positive is None or self.positive,
            min_value=self.min_val,
            max_value=self.max_val
        )

    @staticmethod
    def from_value(value):
        if isinstance(value, (str, float)):
            value = decimal.Decimal(str(value))

        return Decimal().with_values(value)


class StringDecimal(Decimal):
    @property
    def value(self):
        if self._value in [None, '']:
            return self._value

        return f'{float(self._value):.{self.f_len or 2}f}'


class String(Field):
    def __init__(self, name=None, required=True, min_len=1,
                 max_len=None, allow_none=False, default=None, fake_as=None):
        self.save_kwargs(locals())
        self.min_len = min_len
        self.max_len = max_len
        self.fake_as = fake_as
        super().__init__(
            name=name, required=required, allow_none=allow_none,
            default=default
        )

    def generate_value(self):
        return fakeable.fake_string_attr(
            self.fake_as or self.name,
            min_len=self.min_len,
            max_len=self.max_len
        )


class Enum(Field, BaseEnum):
    def __init__(self, name=None, required=True, allow_none=False,
                 default=None, exclude=None):
        self.save_kwargs(locals())
        self.exclude = exclude or ()
        super().__init__(
            name=name, required=required, allow_none=allow_none,
            default=default
        )

    def generate_value(self):
        return random.choice(self.__class__.to_list(
            exclude=self.exclude
        ))


class Raw(String):
    def __init__(self, name=None, required=True, allow_none=False):
        self.save_kwargs(locals())
        self.overrided_values = False
        self._value = None
        super().__init__(
            name=name, required=required, allow_none=allow_none
        )

    def generate_value(self):
        return fakeable.FAKER.pydict(10, True, value_types=(str,))

    def with_values(self, values):
        if self.overrided_values and isinstance(self._value, dict):
            self._value = dictionary.merge_with_updates(self._value, values)
        else:
            self._value = values

        self.overrided_values = True

        return self


class Uuid(Field):
    def generate_value(self):
        return fakeable.FAKER.uuid4()


class DateTime(String):
    def __init__(self, name=None, required=True, allow_none=False,
                 default=None,
                 date_format=dates.Pattern.DATETIME_DELIM_T_WITH_ZONE_PRECISED,
                 rstrip_zeros=False):
        self.save_kwargs(locals())
        self.date_format = date_format
        self.rstrip_zeros = rstrip_zeros
        super().__init__(
            name=name, required=required, allow_none=allow_none,
            default=default
        )

    def generate_value(self):
        return dates.generate_time()

    @property
    def value(self):
        if self._value and not isinstance(self._value, str):
            result = self._value.strftime(self.date_format)

            if self.rstrip_zeros:
                while '0Z' in result:
                    result = result.replace('0Z', 'Z')

            return result

        return self._value

    def to_format(self, date_format, new_tz=None):
        if self._value is None:
            return None

        from_zone = tz.tzutc()
        to_zone = tz.gettz(new_tz)
        value = self._value

        if isinstance(value, str):
            value = datetime.strptime(value, self.date_format)

        local_time = value.replace(tzinfo=from_zone)
        new_time = local_time.astimezone(to_zone)

        return new_time.strftime(date_format)
