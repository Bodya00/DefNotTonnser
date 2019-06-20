from unittest import mock

import pytest

from scraper import parse_param_string, scrape_params, download_page, scrape_company_name, convert_currency


@mock.patch('scraper.requests')
def test_download_page(requests_mock):
    requests_mock.get.return_value.text = 'correct'
    assert download_page('any_url') == 'correct'


def test_parse_param_string():
    with pytest.raises(ValueError) as e:
        assert parse_param_string(" ")
    assert str(e.value) == "Parameter is not money amount", 'Empty string'

    assert parse_param_string("US$21") == 21, 'Minimal accepted string'
    assert parse_param_string("US$21.461") == 21.461, 'Floating point'
    assert parse_param_string("US$21.461 billion") == 21.461 * 10 ** 9, 'Multiplicator'
    assert parse_param_string("US$21.461 billion (2018)") == 21.461 * 10 ** 9, 'Year'
    assert parse_param_string("US$+21.461 billion") == 21.461 * 10 ** 9, 'Plus sign'
    assert parse_param_string("US$-21.461 billion") == -21.461 * 10 ** 9, 'Minus sign'


def test_parse_param_string_check_currency():
    with pytest.raises(ValueError) as e:
        assert parse_param_string("21.461")
    assert str(e.value) == "Parameter is not money amount", 'No currency'

    with pytest.raises(ValueError) as e:
        assert parse_param_string("€9.12")
    assert str(e.value) == "Parameter is not money amount", 'Different currency'


def test_parse_param_string_check_multiplicator():
    with pytest.raises(ValueError) as e:
        assert parse_param_string("US$21.461 lemon")
    assert str(e.value) == "Bad multiplicator", 'Wrong multiplicator'


def test_parse_param_string_check_value():
    with pytest.raises(ValueError) as e:
        assert parse_param_string("US$")
    assert str(e.value) == "Parameter is not money amount", 'No value'


def test_scrape_params():
    html = """
    <html>
    <head></head><body>
    <table class='infobox vcard'><tr>
    <th>Revenue</th><td>US$21</td>
    </tr></table>
    </body></html>
    """
    assert scrape_params(html, ['revenue']) == {'Revenue': 21}, 'Correct html'

    html_wrong = html.replace('US$21', '')
    with pytest.raises(ValueError) as e:
        assert scrape_params(html_wrong, ['revenue'])
    assert str(e.value) == "Parameter Revenue not found in summary table", 'Empty parameter'

    html_wrong = html.replace('<td>US$21</td>', '')
    with pytest.raises(ValueError) as e:
        assert scrape_params(html_wrong, ['revenue'])
    assert str(e.value) == "Parameter Revenue not found in summary table", 'Empty parameter'

    html_wrong = html.replace('Revenue', '')
    with pytest.raises(ValueError) as e:
        assert scrape_params(html_wrong, ['revenue'])
    assert str(e.value) == "Parameter Revenue not found in summary table", 'Empty parameter'

    html_wrong = html.replace('<th>Revenue</th>', '')
    with pytest.raises(ValueError) as e:
        assert scrape_params(html_wrong, ['revenue'])
    assert str(e.value) == "Parameter Revenue not found in summary table", 'Empty parameter'


def test_scrape_company_name():
    company_name = 'DefNotTonnser'
    html = f"""
    <html>
    <head></head><body>
    <table class='infobox vcard'>
    <caption>{company_name}</caption>
    </table>
    </body></html>
    """
    assert scrape_company_name(html) == company_name, 'Correct html'

    html_wrong = html.replace(company_name, '')
    with pytest.raises(ValueError) as e:
        assert scrape_company_name(html_wrong)
    assert str(e.value) == "Caption of summary table not found", 'Empty caption'

    html_wrong = html.replace(f'<caption>{company_name}</caption>', '')
    with pytest.raises(ValueError) as e:
        assert scrape_company_name(html_wrong)
    assert str(e.value) == "Caption of summary table not found", 'No caption'


def test_convert_currency():
    params = {
        'usual': 10,
        'negative': -10,
        'zero': 0
    }
    exchange_rate = {
        'name': 'currency1',
        'exchange_rate': -2
    }
    result = {'usual': -20,
              'negative': 20,
              'zero': 0}
    assert convert_currency(params=params, exchange_rate=exchange_rate) == result, 'correct'
