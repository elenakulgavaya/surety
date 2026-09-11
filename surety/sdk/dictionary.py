import json

from surety.sdk.array import Array
from surety.sdk.field import Field


class _WithValuesDescriptor:
    """Returns a callable that creates a new instance with selective generation.

    Both class and instance call: non-provided fields are auto-generated
    (required only, unless is_full=True). Instance call defaults is_full to
    the instance's own is_full setting and preserves the field's name and kwargs.
    """

    def __get__(self, obj, objtype=None):
        if obj is None:
            def _call(values, is_full=False):
                instance = objtype()
                instance.generate_with_values(values, is_full)
                return instance
            return _call

        default_is_full = obj.is_full

        def _call(values, is_full=None):
            effective_is_full = default_is_full if is_full is None else is_full
            existing = {
                getattr(obj, fn).name: getattr(obj, fn).value
                for fn in obj._get_field_names()
                if getattr(obj, fn).generated
            }
            provided = {
                (k.name if isinstance(k, Field) else k): v
                for k, v in values.items()
            }
            obj.generate_with_values({**existing, **provided}, effective_is_full)
            return obj
        return _call


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

    with_values = _WithValuesDescriptor()

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

        if value is None:
            return

        field_name, field = self._get_field(field_name)

        if isinstance(value, dict):
            setattr(self, field_name, field.with_values(value))

        elif isinstance(value, (list, set)) and isinstance(field, Array):
            new_value = [
                field.field(is_full=self.is_full).with_values(
                    val.value if isinstance(val, Field) else val
                )
                for val in value
            ]
            setattr(self, field_name, type(value)(new_value) if isinstance(value, set) else new_value)
        else:
            setattr(self, field_name, value)

    def apply_values(self, values):
        """Apply provided values to this instance without generating any other fields."""
        for field, value in values.items():
            if isinstance(field, Field):
                field = field.name
            self._set_field_value(field, value)
        return self

    def generate_with_values(self, values, is_full):
        """Selectively generate fields: use provided values where given, generate the rest."""
        self._generated = True
        self._is_none = False

        if self.allow_none and not is_full:
            self._is_none = True
            return

        values_by_name = {
            (k.name if isinstance(k, Field) else k): v for k, v in values.items()
        }

        known_keys = {getattr(type(self), fn).name for fn in self._get_field_names()}
        for key in values_by_name:
            if key not in known_keys:
                raise AttributeError(f'No attribute with name {key}')

        for field_name in self._get_field_names():
            field_template = getattr(type(self), field_name)
            field_key = field_template.name
            val = values_by_name.get(field_key)

            if field_key in values_by_name and val is not None:
                if isinstance(val, dict) and isinstance(field_template, Dictionary):
                    new_field = field_template(is_full=is_full, with_data=False)
                    new_field.generate_with_values(val, is_full)
                    setattr(self, field_name, new_field)
                else:
                    self._set_field_value(field_key, val)
            else:
                if is_full:
                    _with_data = True
                elif field_template.allow_none:
                    _with_data = False
                else:
                    _with_data = field_template.required
                setattr(self, field_name, field_template(is_full=is_full, with_data=_with_data))

        self.generate_custom()

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

            updated = current_value.with_values(value)
            object.__setattr__(self, key, updated)
        else:
            object.__setattr__(self, key, value)
