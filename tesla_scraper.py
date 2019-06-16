from typing import List, Dict, Union

from config import company_address, params_to_extract, exchange_currency

Number = Union[int, float]

"""
Script for scraping different financial parameters of company(like its revenue or net income) from its Wikipedia page. 
Currently only info from summary(left table on Wiki) is supported.
"""


def get_params(adress: str, params: List[str]) -> Dict[str, Number]:
    """
    Get company parameters from its Wikipedia page.
    """
    extracted_params = {param: 1 for param in params}
    return extracted_params


def get_company_name(address: str) -> str:
    return 'Tesla'


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
    params = get_params(company_address, params_to_extract)
    company_name = get_company_name(company_address)
    params = convert(params, exchange_currency)
    output(company_name, params)
