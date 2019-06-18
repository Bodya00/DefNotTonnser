import re
from typing import Union, List, Dict

import bs4 as bs
import requests

from config import multiplicators

Number = Union[int, float]

"""
Script for scraping different financial parameters of company(like its revenue or net income) from its Wikipedia page. 
Currently only info from summary(left table on Wiki) is supported.
"""


def parse_param_string(parameter_string):
    """
    Get number from string of format {currency}{value}{multiplicator}
    """
    parameter_string = parameter_string.replace('\xa0', ' ')

    match = re.search(
            r'(?P<currency>US\$)?'  # currency
            r'(?P<value>[+-]?\d+(?:\.\d+)?)'  # value
            r'(?P<multiplicator>\s[a-zA-Z]*)?',  # billion or million
            parameter_string)

    if not match:
        raise ValueError('Parameter is not numeric')

    currency, value, multiplicator = match.groups(default='')
    if not currency:
        raise ValueError('Bad currency')
    if multiplicator not in multiplicators:
        raise ValueError('Bad multiplicator')
    multiplicator = multiplicator[1:]  # eliminating required space char

    return float(value) * multiplicators[multiplicator]


def scrape_params(html: str, params: List[str]) -> Dict[str, Number]:
    """
    Get company parameters from its Wikipedia page.
    """
    extracted_params = {param: 1 for param in params}
    return extracted_params


def get_company_name(address: str) -> str:
    return 'Tesla'


def download_page(address: str) -> str:
    """Right now it looks more like an alias, but in future way of downloading html_content may be changed"""
    return requests.get(address).text


def convert(params: Dict[str, Number], exchange_rate: Number) -> Dict[str, Number]:
    """
    Convert parameters to other currency.
    """
    converted_params = {name: value * exchange_rate
                        for name, value in params}
    return converted_params


def output(company_name, params: Dict[str, Number]) -> None:
    """Output gathered information"""
    print(f'{company_name}:\n {params}')


if __name__ == '__main__':
    page = download_page(company_address)
    params = scrape_params(page, params_to_extract)
    company_name = get_company_name(company_address)
    params = convert(params, exchange_currency)
    output(company_name, params)
