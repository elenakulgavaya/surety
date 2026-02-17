import json

from surety.sdk.array import Array
from surety.sdk.field import Field


class Dictionary(Field):
    def __init__(self, name=None, required=True, allow_none=False,
                 is_full=False):
        self._generated = False
        self._is_none = False
        self.save_kwargs(locals())
        self.is_full = is_full
        super().__init__(name, required, allow_none)

    def _get_field_names(self):
        result = []

        for attr_name in dir(self.__class__):
            if attr_name.startswith('_'):
                continue

            if isinstance(getattr(self.__class__, attr_name), Field):
                result.append(attr_name)

        return result

    @property
    def generated(self):
        if self._generated or (self.required and self.allow_none):
            return True

        for field_name in self._get_field_names():
            field_value = getattr(self, field_name)

            if field_value.generated:
                return True

        return False

    @generated.setter
    def generated(self, generated):
        self._generated = generated

    @property
    def value(self):
        if not self.generated or self._is_none:
            return None

        _value = {}

        for field_name in self._get_field_names():
            field_value = getattr(self, field_name)

            if field_value.generated:
                _value[field_value.name] = field_value.value

        return _value

    @property
    def full_value(self):
        if not self.generated or self._is_none:
            return None

        _value = {}

        for field_name in self._get_field_names():
            field_value = getattr(self, field_name)
            _value[field_value.name] = field_value.full_value

        return _value

    def generate_value(self):
        pass

    def generate_custom(self):
        pass

    def with_values(self, values):
        for field, value in values.items():
            if isinstance(field, Field):
                field = field.name
            self._set_field_value(field, value)

        return self

    def _get_field(self, name):
        for field_name in self._get_field_names():
            field = getattr(self, field_name)

            if field.name == name:
                return field_name, field

        raise AttributeError(f'No attribute with name {name}')

    def _set_field_value(self, field_name, value):
        if value is None:
            return

        self._is_none = False

        if isinstance(value, Field):
            value = value.value

        field_name, field = self._get_field(field_name)

        if isinstance(value, dict):
            new_value = field.with_values(value)

            if isinstance(field, Dictionary):
                new_value.generated = True

            setattr(self, field_name, new_value)

        elif isinstance(value, list) and isinstance(field, Array):
            new_value = []

            for val in value:
                if isinstance(val, Field):
                    val = val.value

                new_value.append(
                    field.field(is_full=self.is_full).with_values(val)
                )

            setattr(self, field_name, new_value)
        else:
            setattr(self, field_name, value)

    def _generate(self, is_full=True, with_data=True, required=True,
                  use_default=True):
        self._generated = with_data

        if self.allow_none:
            if not is_full:
                self._is_none = True
                return  # Do not generate fields if None is allowed

            self._is_none = False

        if not required and not is_full:
            with_data = False
            self._generated = False

        for field_name in self._get_field_names():
            value = getattr(self, field_name)
            _with_data = with_data

            if _with_data:
                if isinstance(value, Field):
                    if is_full:
                        _with_data = True
                    elif value.allow_none:
                        _with_data = False
                    else:
                        _with_data = value.required

            setattr(self, field_name, value(
                is_full=is_full, with_data=_with_data
            ))

        if with_data:
            self.generate_custom()

    def generate(self, is_full=False):  # pylint: disable=arguments-renamed
        self._generate(is_full=is_full)

    def __setattr__(self, key, value):
        if hasattr(self, key):
            current_value = getattr(self, key)
        else:
            current_value = None

        def needs_json_loads(current, update):
            dict_needs_load = (isinstance(current, Dictionary) and
                               not isinstance(update, dict))
            list_needs_load = (isinstance(current, Array) and
                               not isinstance(update, (list, set)))

            return dict_needs_load or list_needs_load

        if (isinstance(current_value, Field) and
                not isinstance(value, Field)):
            if needs_json_loads(current=current_value, update=value):
                try:
                    if isinstance(value, bytes):
                        value = value.decode('utf-8')

                    value = json.loads(value)
                except json.JSONDecodeError as ex:
                    raise AttributeError(
                        'Assigning entity to primitive'
                    ) from ex

            current_value.with_values(value)
            object.__setattr__(self, key, current_value)
        else:
            object.__setattr__(self, key, value)
