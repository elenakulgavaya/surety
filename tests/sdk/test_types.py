import decimal
import uuid

from datetime import datetime

from surety.sdk import (
    Bool, DateTime, Decimal, Enum, Float, Int, Raw, String, StringDecimal,
    Uuid, Dictionary
)


def test_generate_bool():
    value = Bool().value
    assert isinstance(value, bool)


def test_generate_int():
    value = Int().value
    assert isinstance(value, int)


def test_generate_float():
    value = Float().value
    assert isinstance(value, float)


def test_generate_decimal():
    value = Decimal().value
    assert isinstance(value, decimal.Decimal)


def test_decimal_from_str_value():
    value = Decimal.from_value('2.02').value
    assert isinstance(value, decimal.Decimal)


def test_decimal_from_float_value():
    value = Decimal.from_value(1.9).value
    assert isinstance(value, decimal.Decimal)


def test_generate_string_decimal():
    value = StringDecimal().value
    assert isinstance(value, str)


def test_generate_string_decimal_value():
    value = StringDecimal().value
    assert isinstance(decimal.Decimal(value), decimal.Decimal)


def test_string_decimal_no_value():
    value = StringDecimal().with_values('').value
    assert value == ''


def test_generate_string():
    value = String().value
    assert isinstance(value, str)


def test_generate_enum():
    class EnumVals(Enum):
        Example = 'example'

    assert EnumVals().value == 'example'


def test_enum_to_list():
    class EnumVals(Enum):
        Value1 = 'val_1'
        Value2 = 'val_2'
        Value3 = 'val_3'

    assert EnumVals.to_list() == ['val_1', 'val_2', 'val_3']


def test_enum_to_list_exclude_value():
    class EnumVals(Enum):
        Value1 = 'val_1'
        Value2 = 'val_2'
        Value3 = 'val_3'

    assert EnumVals.to_list(exclude=EnumVals.Value2) == ['val_1', 'val_3']


def test_enum_to_list_exclude_multiple_values():
    class EnumVals(Enum):
        Value1 = 'val_1'
        Value2 = 'val_2'
        Value3 = 'val_3'

    assert EnumVals.to_list(
        exclude=(EnumVals.Value2, EnumVals.Value3)
    ) == ['val_1']


def test_generate_raw():
    value = Raw().value
    assert isinstance(value, dict)


def test_raw_with_values():
    value = Raw().with_values({'test': 123}).value
    assert value == {'test': 123}


def test_raw_with_values_override():
    value = Raw().with_values({
        'first': 'val1',
        'second': 'val2',
        'third': 'val3'
    }).with_values({'second': 'val_two'}).value
    assert value == {
        'first': 'val1',
        'second': 'val_two',
        'third': 'val3'
    }


def test_generate_datetime_type():
    value = DateTime().value
    assert isinstance(value, str)


def test_generate_datetime_type_trailing_zeroes():
    expected = '2026-02-10T09:07:11.404000Z'
    value = DateTime().with_values(expected).value
    assert value == expected


def test_generate_datetime_type_rstrip_trailing_zeroes():
    initial = '2026-02-10T09:07:11.404000Z'
    expected = '2026-02-10T09:07:11.404Z'
    set_value = datetime.strptime(initial, '%Y-%m-%dT%H:%M:%S.%fZ')
    value = DateTime(rstrip_zeros=True).with_values(set_value).value
    assert value == expected

def test_datetime_to_format_no_value():
    class OptionalDateTime(Dictionary):
        DateTime = DateTime(name='date_time', required=False)

    value = OptionalDateTime().DateTime.to_format('%Y-%m-%dT%H:%M:%S.%fZ')
    assert value is None

def test_datetime_to_format():
    initial = '2026-02-10T09:07:11.404000Z'
    expected = '2026-10-02'
    set_value = datetime.strptime(initial, '%Y-%m-%dT%H:%M:%S.%fZ')
    value = DateTime().with_values(set_value).to_format('%Y-%d-%m')
    assert value == expected


def test_datetime_to_format_from_string():
    initial = '2026-02-10T09:07:11.404000Z'
    expected = '09:07:11'
    value = DateTime().with_values(initial).to_format('%H:%M:%S', new_tz='utc')

    assert value == expected


def test_generate_uuid_type():
    value = Uuid().value
    assert isinstance(value, str)


def test_generate_uuid_value():
    value = Uuid().value
    assert isinstance(uuid.UUID(value, version=4), uuid.UUID)
