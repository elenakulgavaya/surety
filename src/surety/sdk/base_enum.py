
class BaseEnum:
    @classmethod
    def _attr_values_as_list(cls):
        result = []

        for attr_name in dir(cls):
            if not attr_name.startswith('_'):
                attr_value = getattr(cls, attr_name)

                if (not callable(attr_value) and
                        not isinstance(attr_value, property)):
                    result.append(attr_value)

        return result

    @classmethod
    def to_list(cls, exclude=()):
        """
        :param exclude: list of values to be excluded from result; if
          not existent value passed, ValueError exception will be thrown
        :return: list of all fields of class A(Enum) and its parents
        """
        result = cls._attr_values_as_list()
        if type(exclude) not in (list, tuple):
            exclude = (exclude,)

        for item in exclude:
            result.remove(item)

        return result
