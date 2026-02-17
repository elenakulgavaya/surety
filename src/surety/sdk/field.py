from abc import ABCMeta, abstractmethod


class Field(metaclass=ABCMeta):
    def __init__(self, name=None, required=True, allow_none=False,
                 default=None):
        self.required = required
        self.allow_none = allow_none
        self.name = name
        self.default = default
        self._value = None

        if not hasattr(self, '_kwargs'):
            self.save_kwargs(locals())

        if not hasattr(self, 'is_full'):
            self.is_full = True

        if name is None:
            self._generate(is_full=self.is_full)
        else:
            self._generate(with_data=False)

    def save_kwargs(self, local_vars):
        if hasattr(self, '_kwargs'):
            return

        self._kwargs = {k: v for k, v in local_vars.items()
                        if k not in ('self', '__class__')}

    @property
    def generated(self):
        if self._value is None:
            return self.required and self.allow_none

        return True

    @property
    def value(self):
        return self._value

    @property
    def full_value(self):
        return self.value

    def __call__(self, is_full, with_data=True):
        new_instance = self.__class__(**self._kwargs)
        new_instance._generate(is_full=is_full, with_data=with_data,
                               required=new_instance.required)

        return new_instance

    def with_values(self, values):
        self._value = values

        return self

    def _generate(self, is_full=True, with_data=True, required=True,
                  use_default=True):
        if not with_data:
            return

        if is_full or (required and not self.allow_none):
            if use_default and self.default is not None:
                if callable(self.default):
                    self._value = self.default()
                else:
                    self._value = self.default
            else:
                self._value = self.generate_value()

    def generate(self, use_default=False):
        self._generate(use_default=use_default)

    @abstractmethod
    def generate_value(self):
        """Valid value generator based on type"""

    def __repr__(self):
        return str(self.value)
