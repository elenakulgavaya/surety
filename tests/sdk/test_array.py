from surety.sdk import Array, Set, String


def test_array_no_generate_value():
    assert Array(String).generate_value() is None


def test_array_generate():
    array = Array(String)
    array.generate()
    assert isinstance(array.value, list)


def test_array_generate_value():
    value = Array(String).value
    assert isinstance(value, list)


def test_len_of_array():
    generated_array = Array(String, max_len=3, min_len=3)
    assert len(generated_array) == 3


def test_set_array_value():
    generated_array = Array(String, min_len=1, max_len=1)
    generated_array[0] = String(default='test')
    assert generated_array.value == ['test']


def test_iterate_by_array():
    generated_array = Array(String(default='test'), min_len=1, max_len=1)
    result = []

    for item in generated_array:
        result.append(item.value)

    assert result == ['test']


def test_append():
    generated_array = Array(String(default='test'), min_len=1, max_len=1)
    generated_array.append(String(default='test2'))
    assert generated_array.value == ['test', 'test2']


def test_with_values():
    generated_array = Array(String).with_values([
        'test1', 'test2', 'test3'
    ])
    assert generated_array.value == ['test1', 'test2', 'test3']


def test_with_no_values():
    array = Array(
        String(default='test'), min_len=1, max_len=1
    )
    array.with_values('')
    assert array.value == []


def test_set_with_no_values():
    new_set = Set(
        String(default='test'), min_len=1, max_len=1
    )
    new_set.with_values('')
    assert new_set.value == set()
