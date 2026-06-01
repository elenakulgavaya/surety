from surety.sdk import fakeable
from surety.sdk.fakeable import (
    fake, fake_string_attr, generate_float, generate_string,
    _to_snake_case, _resolve_faker_provider,
)


def test_generate_string_fixed_size():
    value = generate_string(size=28)
    assert len(value) == 28


def test_fake_attribute():
    value = fake_string_attr('company_email')
    assert '@' in value


def test_fake_attribute_sentences():
    value = fake_string_attr('sentences')
    assert '\n' in value


def test_max_len_in_fake_attrs():
    value = fake_string_attr('uuid4', max_len=10)
    assert len(value) == 10


def test_generate_float_i_len():
    value = generate_float(i_len=3)
    assert len(str(value).split('.', maxsplit=1)[0]) <= 3


def test_generate_float_f_len():
    value = generate_float(f_len=5)
    assert len(str(value).split('.')[1]) <= 5


def test_generate_float_fixed_f_len(monkeypatch):
    monkeypatch.setattr(
        fakeable.random,
        'randint',
        lambda x, y: 1 if y < 10 else 10
    )
    value = generate_float(fixed_f_len=True, f_len=2, i_len=0,
                           integer_allowed=False)
    assert len(str(value).split('.')[1]) == 2


def test_snake_case_camel():
    assert _to_snake_case('phoneNumber') == 'phone_number'


def test_snake_case_title():
    assert _to_snake_case('CurrencyCode') == 'currency_code'


def test_snake_case_already_snake():
    assert _to_snake_case('phone_number') == 'phone_number'


def test_snake_case_single_word():
    assert _to_snake_case('email') == 'email'


def test_resolve_layer1_direct_match():
    assert _resolve_faker_provider('email') == 'email'


def test_resolve_camel_case():
    assert _resolve_faker_provider('phoneNumber') == 'phone_number'


def test_resolve_title():
    assert _resolve_faker_provider('CurrencyCode') == 'currency_code'


def test_resolve_semantic_alias():
    assert _resolve_faker_provider('description') == 'sentences'


def test_resolve_suffix_id():
    assert _resolve_faker_provider('providerId') == 'uuid4'


def test_resolve_suffix_url():
    assert _resolve_faker_provider('attachment_url') == 'url'


def test_resolve_email():
    assert _resolve_faker_provider('contactEmail') == 'email'


def test_resolve_none_for_unknown():
    assert _resolve_faker_provider('abc') is None


def test_resolve_none_for_empty():
    assert _resolve_faker_provider(None) is None


def test_fake_non_callable_attr():
    assert isinstance(fake.locales, list)


def test_fake_direct_call_word():
    assert isinstance(fake.word(), str)


def test_fake_direct_call_email():
    assert '@' in fake.email()


def test_unit_returns_full_name():
    assert fake.unit() in [
        'Bottle', 'Box', 'Can', 'Case', 'Feet', 'Gallon', 'Gram',
        'Inches', 'Kilogram', 'Pounds', 'Liter', 'Milliliter',
        'Millimeter', 'Meter', 'Ounces', 'Pieces',
    ]


def test_unit_code_returns_code():
    assert fake.unit_code() in [
        'BOT', 'BOX', 'CAN', 'CS', 'FT', 'GA', 'GR',
        'IN', 'KG', 'LB', 'LTR', 'ML', 'MM', 'MTR', 'OZ', 'PCS',
    ]


def test_calories_format():
    assert fake.calories().endswith('kcal')


def test_fat_format():
    assert fake.fat().endswith('g')


def test_saturated_fat_format():
    assert fake.saturated_fat().endswith('g')


def test_protein_format():
    assert fake.protein().endswith('g')


def test_sodium_format():
    assert fake.sodium().endswith('mg')


def test_carbohydrates_format():
    assert fake.carbohydrates().endswith('g')


def test_sugar_format():
    assert fake.sugar().endswith('g')


def test_salt_format():
    assert fake.salt().endswith('g')


def test_cholesterol_format():
    assert fake.cholesterol().endswith('mg')


def test_fiber_format():
    assert fake.fiber().endswith('g')


def test_fake_string_returns_alphanumeric():
    value = fake.string()
    assert isinstance(value, str)
    assert 1 <= len(value) <= 20


def test_fake_string_respects_bounds():
    value = fake.string(min_chars=5, max_chars=10)
    assert 5 <= len(value) <= 10


def test_fake_number_returns_int_string():
    value = fake.number()
    assert isinstance(value, str)
    assert 0 <= int(value) <= 9999


def test_fake_number_respects_bounds():
    value = fake.number(min_value=100, max_value=200)
    assert 100 <= int(value) <= 200


def test_max_len_truncates_result():
    value = fake.sentence(max_len=10)
    assert len(value) <= 10


def test_max_len_strips_trailing_spaces():
    value = fake.sentence(max_len=5)
    assert not value.endswith(' ')


def test_max_len_no_truncation_when_shorter():
    value = fake.word(max_len=1000)
    assert len(value) <= 1000


def test_invalid_provider_warns_and_returns_string():
    import warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        value = fake.postal_code()
    assert len(w) == 1
    assert 'postal_code' in str(w[0].message)
    assert isinstance(value, str)
    assert len(value) > 0


def test_invalid_provider_respects_max_len():
    import warnings
    with warnings.catch_warnings(record=True) as w:
        warnings.simplefilter('always')
        value = fake.postal_code(max_len=5)
    assert len(value) <= 5
