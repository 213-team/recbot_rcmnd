import logging
import os
import pickle

import requests
from bs4 import BeautifulSoup

from conf.config import Conf
from constants import (
    TELEGRAM_CHANNEL_TO_CATEGORY_FILE,
    CATEGORY_TO_TELEGRAM_CHANNEL_FILE
)

logging.basicConfig(level=logging.INFO)


def collect_channels_categories() -> dict:
    """Collect all possible channels categories

    :return: {'channel_category': {'href': ..., 'channels': {}}}
    """
    dict_of_channels_categories = dict()
    page = requests.get('https://tlgrm.ru/channels')
    soup = BeautifulSoup(page.content, 'html.parser')
    for channel_category in soup.find_all('a', class_='channel-category'):
        dict_of_channels_categories[channel_category['data-topic']] = dict()
        dict_of_channels_categories[channel_category['data-topic']]['href'] = channel_category['href']
        dict_of_channels_categories[channel_category['data-topic']]['channels'] = dict()
    return dict_of_channels_categories


def collect_category_channels(category_name: str, dict_of_channels_categories: dict, num_of_pages: int = 500):
    """Collect channels info by going through all channels in some category

    :param category_name:
    :param dict_of_channels_categories:
    :param num_of_pages: how deep we go through each category
    :return:
    """
    # 0 - is an advert; skip it
    for page_id in range(1, num_of_pages):
        href = dict_of_channels_categories[category_name]['href']
        page = requests.get(href + '?page={}'.format(page_id))
        soup = BeautifulSoup(page.content, 'html.parser')
        channel_cards = soup.find_all('div', class_='channel-card')
        if channel_cards:
            for channel_card in channel_cards[1:]:
                href = channel_card.find('a', class_='channel-card__username')['href']
                number_of_subscribers = int(channel_card
                                            .find('span', class_='channel-card__subscribers')
                                            .get_text()
                                            .strip().replace(" ", "")
                                            .replace(' ', ''))
                if '@' in href:
                    channel_key = 't.me/' + href.split('@')[1]
                else:
                    try:
                        channel_key = 't.me/' + href.split('=')[1]
                    except IndexError:
                        continue
                dict_of_channels_categories[category_name]['channels'][channel_key] = number_of_subscribers
        else:
            logging.info(f"{category_name}, {page_id}")
            break


if __name__ == '__main__':
    channels_categories = collect_channels_categories()
    for key in channels_categories:
        collect_category_channels(key, channels_categories)
    with open(os.path.join(Conf.PATH_TO_DATA, CATEGORY_TO_TELEGRAM_CHANNEL_FILE), 'wb') as f:
        pickle.dump(channels_categories, f)

    channel2category = dict()
    for category in channels_categories:
        for channel in channels_categories[category]['channels']:
            channel2category[channel] = category

    with open(os.path.join(Conf.PATH_TO_DATA, TELEGRAM_CHANNEL_TO_CATEGORY_FILE), 'wb') as f:
        pickle.dump(channel2category, f)
