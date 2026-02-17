from surety.sdk.base_enum import BaseEnum


def test_base_enum_single_value_to_list():
    class SingleVal(BaseEnum):
        First = 'first'

    assert SingleVal.to_list() == ['first']


def test_base_enum_multiple_values_to_list():
    class MultiVal(BaseEnum):
        First = 'first'
        Second = 'second'

    assert MultiVal.to_list() == ['first', 'second']


def test_base_enum_skip_others_in_to_list():
    class ExtrasVal(BaseEnum):
        First = 'first'
        Second = 'second'

        @property
        def prop_first(self):
            return None

        def method_first(self):
            return self

    assert ExtrasVal.to_list() == ['first', 'second']


def test_base_enum_exclude():
    class Values(BaseEnum):
        First = 'first'
        Second = 'second'
        Third = 'third'
        Last = 'last'

    assert sorted(Values.to_list(exclude=Values.Third)) == sorted(
        ['first', 'second', 'last']
    )


def test_base_enum_exclude_multiple():
    class Values(BaseEnum):
        First = 'first'
        Second = 'second'
        Third = 'third'
        Last = 'last'

    assert sorted(Values.to_list(
        exclude=[Values.Third, Values.First]
    )) == sorted(['second', 'last'])
