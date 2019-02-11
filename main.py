import argparse
import os
import requests
from dotenv import load_dotenv

from utils import error_print, success_print


BITLY_BASE_API_URL = 'https://api-ssl.bitly.com/v4/'


def get_headers(token: str) -> dict:
    return {
        'Authorization': f'Bearer {token}',
    }


def get_bitlink(long_url: str, token: str) -> str:
    shortener_url = f'{BITLY_BASE_API_URL}bitlinks'
    payload = {
        'long_url': long_url
    }
    response = requests.post(
        shortener_url,
        headers=get_headers(token),
        json=payload
    )
    response.raise_for_status()
    return str(response.json()['link'])


def get_click_count(bitlink: str, token: str, units=-1) -> str:
    click_count_url = \
        f'{BITLY_BASE_API_URL}bitlinks/{bitlink}/clicks/summary'
    payload = {
        'unit': 'day',
        'units': units  # -1 by default, returns result for all time
    }
    response = requests.get(
        click_count_url,
        headers=get_headers(token),
        params=payload
    )
    response.raise_for_status()
    return str(response.json()['total_clicks'])
    

def is_bitlink(link: str, token: str) -> bool:
    check_bitlink_url = f'{BITLY_BASE_API_URL}bitlinks/{link}'
    response = requests.get(
        check_bitlink_url,
        headers=get_headers(token)
    )
    return response.ok


def get_args():
    """Parse command line."""
    parser = argparse.ArgumentParser(
        description='Returns short bitlink for any given link, '
                    'and usage statistics for a given bitlink.'
    )
    parser.add_argument(
        'url',
        help='A link for reduction or bitlink to get statistics'
    )
    args = parser.parse_args()
    return args


def main() -> None:
    load_dotenv()
    token = os.getenv('TOKEN')
    raw_link = get_args().url

    if not raw_link:
        error_print('Your link is empty. Try again.')
        exit()

    try:
        protocol, link = raw_link.split('://') \
            if 'http' in raw_link else ('http', raw_link)
    except ValueError:
        error_print('Wrong url format. Try again.')
        exit()

    try:
        if is_bitlink(link, token):
            success_print('This link has been clicked {} times.'.format(
                get_click_count(link, token)
            ))
        else:
            success_print('This is your very short link: {}'.format(
                get_bitlink(f'{protocol}://{link}', token)
            ))
    except requests.exceptions.HTTPError as e: 
        if e.response.status_code == 400:
            error_print(e.response.json()['description'])
        else:
            error_print(str(e))


if __name__ == '__main__':
    main()
