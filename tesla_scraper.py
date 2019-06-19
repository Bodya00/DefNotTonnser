import re
from typing import Union, List, Dict

import bs4 as bs
import requests

from config import multiplicators, company_address, params_to_extract, exchange_rate

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
            r'(?:US\$)'  # currency
            r'(?P<value>[+−-]?\d+(?:\.\d+)?)'  # value, minus sign can be written as − or -
            r'(?P<multiplicator>\s[a-zA-Z]*)?',  # billion or million
            parameter_string)

    if not match:
        raise ValueError('Parameter is not money amount')

    value, multiplicator = match.groups(default='')
    value = value.replace('−', '-')  # minus sign can be written as − or -
    multiplicator = multiplicator[1:]  # eliminating required space char

    if multiplicator not in multiplicators:
        raise ValueError('Bad multiplicator')

    return float(value) * multiplicators[multiplicator]


def scrape_params(html: str, params: List[str]) -> Dict[str, Number]:
    """
    Get company parameters from summary_table on its Wikipedia page.
    """
    params = [param.capitalize() for param in params]
    page = bs.BeautifulSoup(html, 'html.parser')
    extracted_params = {}
    summary_table = page.find('table',  # find one summary table
                              class_='infobox vcard')

    if not summary_table:
        raise ValueError('No summary table found')

    for param in params:
        try:
            param_string = summary_table.find('th', text=param  # find header of parameter in summary table
                                              ).next_sibling.text  # get parameter from that header
        except AttributeError:
            raise ValueError(f'Parameter {param} not found in summary table')
        if not param_string:
            raise ValueError(f'Parameter {param} not found in summary table')

        extracted_params[param] = parse_param_string(param_string)

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
