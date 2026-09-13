import random

from surety.sdk.field import Field


class _ArrayWithValuesDescriptor:
    def __get__(self, obj, objtype=None):
        if obj is None:
            def _call(values):
                instance = objtype(_with_data=False)
                return instance.apply_values(values)
            return _call

        def _call(values):
            return obj.apply_values(values)
        return _call


class Array(Field):
    def __init__(self, field, name=None, required=True, allow_none=False,
                 is_full=False, min_len=1, max_len=1, _with_data=True):
        if not hasattr(self, '_kwargs'):
            self.save_kwargs(locals())

        self.is_full = is_full
        self._field = field
        self.min_len = min_len
        self.max_len = max_len
        self._value = None
        super().__init__(name, required, allow_none, _with_data=_with_data)

    @property
    def field(self):
        if not isinstance(
                self._field, Field) and issubclass(self._field, Field):
            self._field = self._field()

        return self._field

    @property
    def value(self):
        if self._value is None:
            return None

        return [field.value for field in self._value]

    @property
    def full_value(self):
        if self._value is None:
            return []

        return [field.full_value for field in self._value]

    def generate_value(self):
        pass

    def _generate(self, is_full=False, with_data=True, required=True,
                  use_default=None):
        # Not processed: duplicated entities, duplicated empty dicts
        if with_data and (is_full or required):
            self._value = [self.field(is_full=is_full) for _ in range(
                random.randint(self.min_len, self.max_len)
            )]

    def generate(self, is_full=False):  # pylint: disable=arguments-renamed
        self._generate(is_full=is_full)

    def __len__(self):
        return len(self._value)

    def __getitem__(self, item):
        return self._value[item]  # Return Field to provide attribute access

    def __setitem__(self, key, value):
        self._value[key] = value

    def __iter__(self):
        return iter(self._value)

    def append(self, value):
        self._value.append(value)

    def apply_values(self, values):
        if isinstance(values, list):
            _values = []

            for value in values:
                if not isinstance(value, self.field.__class__):
                    v = value.value if isinstance(value, Field) else value
                    value = self.field(is_full=False).with_values(v)
                _values.append(value)
            self._value = _values

            return self

        return super().with_values(values)

    with_values = _ArrayWithValuesDescriptor()


class Set(Array):
    def apply_values(self, values):
        if isinstance(values, (set, list)):
            _values = set()

            for value in values:
                if not isinstance(value, self.field.__class__):
                    v = value.value if isinstance(value, Field) else value
                    value = self.field(is_full=False).with_values(v)
                _values.add(value)
            self._value = _values

            return self

        return super().apply_values(values)

    @property
    def value(self):
        if self._value is None:
            return None

        return {field.value for field in self._value}

    @property
    def full_value(self):
        if self._value is None:
            return []

        return {field.full_value for field in self._value}
