from surety.sdk import fakeable

from surety.sdk.fakeable import (
    Fakeable, fake_string_attr, generate_float, generate_string,
)


def test_generate_string_fixed_size():
    value = generate_string(size=28)
    assert len(value) == 28


def test_fake_attribute():
    value = fake_string_attr(Fakeable.CompanyEmail)
    assert '@' in value


def test_max_len_in_fake_attrs():
    value = fake_string_attr(Fakeable.Uuid, max_len=10)
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


def test_fakeable_to_list():
    assert len(Fakeable.to_list()) == 81


def test_fakeable_include():
    assert Fakeable.AmPm in Fakeable.to_list()


def test_fakeable_exclude():
    assert len(Fakeable.to_list(exclude=[
        Fakeable.AmPm, Fakeable.Address, Fakeable.CompanyEmail
    ])) == 78


def test_fakeable_exclude_value():
    assert Fakeable.DateTime not in Fakeable.to_list(exclude=Fakeable.DateTime)
