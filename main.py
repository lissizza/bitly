import argparse
import os
import requests
from dotenv import load_dotenv

from utils import error_print, success_print

load_dotenv()


BITLY_BASE_API_URL = 'https://api-ssl.bitly.com/v4/'
TOKEN = os.getenv('TOKEN')


def get_headers(token: str) -> dict:
    return {
        'Authorization': f'Bearer {token}',
    }


def get_shortener_response(long_url: str, token=TOKEN) -> requests.Response:
    shortener_url = f'{BITLY_BASE_API_URL}bitlinks'
    payload = {
        'long_url': long_url
    }
    response = requests.post(
        shortener_url,
        headers=get_headers(token),
        json=payload
    )
    return response


def get_click_count_response(bitlink: str, token=TOKEN) -> requests.Response:
    click_count_url = f'{BITLY_BASE_API_URL}bitlinks/{bitlink}/clicks/summary'
    payload = {
        'unit': 'day',
        'units': '' 
    }
    response = requests.get(
        click_count_url,
        headers=get_headers(token),
        params=payload
    )
    return response
    

def is_bitlink(link: str, token=TOKEN) -> bool:
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
    raw_link = get_args().url

    if not raw_link:
        print('Your link is empty. Try again.')
        exit()

    protocol, link = (raw_link.split('://')) \
        if 'http' in raw_link else ('http', raw_link)

    if is_bitlink(link):
        response = get_click_count_response(link)
        key = 'total_clicks'
        message = 'This link has been clicked {} times.'
    else:
        response = get_shortener_response(f'{protocol}://{link}')
        key = 'link'
        message = 'This is your very short link: {}'

    if response.ok:
        success_print(message.format(response.json()[key]))
        exit()
    
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e: 
        if e.response.status_code == 400:
            message = response.json()['description']
        else:
            message = e
        error_print(message)


if __name__ == '__main__':
    main()
