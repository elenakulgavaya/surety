import decimal
import random
import re

from faker import Faker

from surety.sdk.base_enum import BaseEnum
from surety.sdk.providers.nutrition import NutritionProvider
from surety.sdk.providers.units import UnitsProvider


def _to_snake_case(name):
    s1 = re.sub(r'([A-Z]+)([A-Z][a-z])', r'\1_\2', name)
    return re.sub(r'([a-z\d])([A-Z])', r'\1_\2', s1).lower()


fake = Faker()
fake.add_provider(UnitsProvider)
fake.add_provider(NutritionProvider)

FAKER = fake  # backward compatibility

class Fakeable(BaseEnum):  # backward compatibility
    Address = 'address'
    AmPm = 'am_pm'
    AndroidToken = 'android_platform_token'
    BankCountry = 'bank_country'
    Boolean = 'boolean'
    BuildingNumber = 'building_number'
    City = 'city'
    CityPrefix = 'city_prefix'
    CitySuffix = 'city_suffix'
    ColorName = 'color_name'
    SafeColorName = 'safe_color_name'
    Company = 'company'
    CompanyEmail = 'company_email'
    Coordinate = 'coordinate'
    Country = 'country'
    CountryCode = 'country_code'
    CreditCardExpire = 'credit_card_expire'
    CreditCardFull = 'credit_card_full'
    CreditCardNumber = 'credit_card_number'
    CreditCardProvider = 'credit_card_provider'
    CreditCardSecurityCode = 'credit_card_security_code'
    Currency = 'currency'
    CurrencyCode = 'currency_code'
    CurrencyName = 'currency_name'
    Date = 'date'
    DateOfBirth = 'date_of_birth'
    DateThisMonth = 'date_this_month'
    DateTime = 'date_time'
    DayOfMonth = 'day_of_month'
    DomainName = 'domain_name'
    Email = 'email'
    FileExtension = 'file_extension'
    FileName = 'file_name'
    FirstName = 'first_name'
    FutureDate = 'future_date'
    FutureDateTime = 'future_datetime'
    HexColor = 'hex_color'
    Hostname = 'hostname'
    Iban = 'iban'
    ImageUrl = 'image_url'
    IosToken = 'ios_platform_token'
    LastName = 'last_name'
    Latitude = 'latitude'
    Longitude = 'longitude'
    Month = 'month'
    MonthName = 'month_name'
    Name = 'name'
    Password = 'password'
    PastDate = 'past_date'
    PastDateTime = 'past_datetime'
    PhoneNumber = 'phone_number'
    PostalCode = 'postalcode'
    Decimal = 'pydecimal'
    Dict = 'pydict'
    Float = 'pyfloat'
    Iterable = 'pyiterable'
    List = 'pylist'
    Str = 'pystr'
    Digit = 'random_digit'
    Int = 'random_int'
    Number = 'random_number'
    SecondaryAddress = 'secondary_address'
    Sentence = 'sentence'
    Sentences = 'sentences'
    State = 'state'
    StateAbbr = 'state_abbr'
    StreetAddress = 'street_address'
    StreetName = 'street_name'
    Text = 'text'
    Time = 'time'
    TimeDelta = 'time_delta'
    Timezone = 'timezone'
    UnixTime = 'unix_time'
    Url = 'url'
    UserName = 'user_name'
    Uuid = 'uuid4'
    Word = 'word'
    Year = 'year'
    Zipcode = 'zipcode'
    RgbColor = 'rgb_color'
    RgbCssColor = 'rgb_css_color'

_SEMANTIC_ALIASES = {
    'currency': 'currency_code',
    'description': 'sentences',
    'subject': 'sentence',
    'note': 'sentence',
    'notes': 'sentences',
    'comment': 'sentence',
    'comments': 'sentences',
    'information': 'sentence',
    'details': 'sentence',
    'title': 'sentence',
    'text': 'text',
    'content': 'text',
    'body': 'text',
    'filename': 'file_name',
    'brand': 'company',
    'manufacturer': 'company',
    'carbohydrates': 'carbohydrates',
    'line1': 'name',
    'line2': 'street_address',
    'line3': 'secondary_address',
    'line4': 'postalcode',
}
_SUFFIX_PATTERNS = [
    ('_url', 'url'),
    ('_email', 'email'),
    ('_phone', 'phone_number'),
    ('_line1', 'street_address'),
    ('_line2', 'secondary_address'),
    ('_line3', 'postal_code'),
    ('_address', 'street_address'),
    ('_city', 'city'),
    ('_country', 'country'),
    ('_name', 'name'),
    ('_id', 'uuid4'),
    ('_number', 'number'),
    ('_owner', 'name'),
    ('_currency', 'currency_code'),
    ('_unit_code', 'unit_code'),
    ('_unit', 'unit'),
]


def _resolve_faker_provider(name):
    if not name:
        return None

    if hasattr(fake, name):
        return name

    snake = _to_snake_case(name)
    if hasattr(fake, snake):
        return snake

    if snake in _SEMANTIC_ALIASES:
        return _SEMANTIC_ALIASES[snake]

    for suffix, provider in _SUFFIX_PATTERNS:
        if snake.endswith(suffix):
            return provider

    return None


def generate_string(size=None, min_len=None, max_len=None):
    if size is not None:
        min_len = size
        max_len = size

    return fake.pystr(min_chars=min_len, max_chars=max_len or 20)


def fake_string_attr(attr_name, min_len=None, max_len=None):
    provider = _resolve_faker_provider(attr_name)

    if provider:
        result = getattr(fake, provider)()

        if isinstance(result, list):
            result = '\n'.join(result)
        else:
            result = str(result)

        if max_len and len(result) > max_len:
            result = result[:max_len]

        return result

    return generate_string(min_len=min_len, max_len=max_len)


def generate_float(i_len=None, f_len=None, integer_allowed=True, max_val=None,
                   fixed_f_len=False, i_min=None):
    """
      Generates a random float with a floating number of digits in integer and
    fractional part. Fractional part length can be fixed for e.g. money types.
      Cannot be used with f_len=1 & fixed_f_len=True - fraction part will be 0
    :param i_len: max length of integer part
    :param f_len: max length of fraction part
    :param integer_allowed: whether float might end with zero like 21.0
    :type max_val: int or None
    :param max_val: max allowed value, result will be generated up to the value
      specified (never equal)
    :param fixed_f_len: whether length of floating part is fixed
    :param i_min: min value of integer part, default value is 0
    """
    f_len = 6 if f_len is None else f_len
    i_max = max_val or 10 ** (3 if i_len is None else i_len)
    f_max = 10 ** f_len
    f_min = 0 if integer_allowed else 1
    i_min = i_min or 0
    i_part = random.randint(i_min, i_max - 1)
    f_part = random.randint(f_min, f_max - 1)

    if fixed_f_len and f_part % 10 == 0:
        f_part += random.randint(1, 9)

    return float(i_part + f_part / decimal.Decimal(f_max))
