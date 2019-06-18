import pytest

from tesla_scraper import parse_param_string


def test_download_page():
    # start simple http server and test on it
    pass


def test_parse_param_string():
    assert parse_param_string("US$21") == 21, 'Minimal accepted string'
    assert parse_param_string("US$21.461") == 21.461, 'Floating point'
    assert parse_param_string("US$21.461 billion") == 21.461 * 10 ** 9, 'Multiplicator'
    assert parse_param_string("US$21.461 billion (2018)") == 21.461 * 10 ** 9, 'Year'
    assert parse_param_string("US$+21.461 billion") == 21.461 * 10 ** 9, 'Plus sign'
    assert parse_param_string("US$-21.461 billion") == -21.461 * 10 ** 9, 'Minus sign'
    assert parse_param_string("US$21.+-461") == 21


def test_parse_param_string_check_currency():
    with pytest.raises(ValueError) as e:
        assert parse_param_string("21.461")
    assert str(e.value) == "Bad currency", 'No currency'

    with pytest.raises(ValueError) as e:
        assert parse_param_string("€9.12")
    assert str(e.value) == "Bad currency", 'Different currency'


def test_parse_param_string_check_multiplicator():
    with pytest.raises(ValueError) as e:
        assert parse_param_string("US$21.461 lemon")
    assert str(e.value) == "Bad multiplicator", 'Wrong multiplicator'


def test_parse_param_string_check_value():
    with pytest.raises(ValueError) as e:
        assert parse_param_string("US$")
    assert str(e.value) == "Parameter is not numeric", 'No value'
    # todo add wrong value tests
