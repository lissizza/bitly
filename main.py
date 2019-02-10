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


def get_shortener_response(
    long_url: str,
    token: str
) -> requests.Response:
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


def get_click_count_response(
    bitlink: str,
    token: str,
    units=-1
) -> requests.Response:
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
    return response
    

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


def handle_response(response, key=None):
    try:
        response.raise_for_status()
        return str(response.json()[key])
    except requests.exceptions.HTTPError as e: 
        if e.response.status_code == 400:
            return response.json()['description']
        else:
            return str(e)


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

    if is_bitlink(link, token):
        response = get_click_count_response(link, token)
        result = handle_response(response, 'total_clicks')
    else:
        response = get_shortener_response(f'{protocol}://{link}', token)
        result = handle_response(response, 'link')

    success_print(result) if response.ok else error_print(result)


if __name__ == '__main__':
    main()
