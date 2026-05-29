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


def test_fake_direct_call():
    assert isinstance(fake.word(), str)
    assert isinstance(fake.email(), str)
    assert '@' in fake.email()
