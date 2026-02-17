from tests.data import Mix


def test_generated_array_is_full_false():
    mix_full = Mix(is_full=True)
    assert mix_full.OptBaseArray[0].is_full is False


def test_generated_array_is_full_true():
    mix = Mix()
    assert mix.ReqFullBaseArray[0].is_full
