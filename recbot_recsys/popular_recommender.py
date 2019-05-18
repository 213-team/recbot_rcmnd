import os
import pickle

from conf.config import Conf
from constants import (
    CATEGORY_TO_TELEGRAM_CHANNEL_FILE,
    TELEGRAM_CHANNEL_TO_CATEGORY_FILE
)


class PopularRecommender:
    """Recommend channels based on their popularity
    """
    def __init__(self):
        with open(os.path.join(Conf.PATH_TO_DATA, CATEGORY_TO_TELEGRAM_CHANNEL_FILE), "rb") as f:
            self.category_to_telegram_channel = pickle.load(f)

        with open(os.path.join(Conf.PATH_TO_DATA, TELEGRAM_CHANNEL_TO_CATEGORY_FILE), "rb") as f:
            self.telegram_channel_to_category = pickle.load(f)

    def recommend(self, user_channels: str) -> list:
        """

        :param user_channels: string of channels separated by ','
        :return:
        """
        user_channels = set(user_channels.split(","))
        user_categories = set([self.telegram_channel_to_category[channel] for channel in user_channels])
        dict_of_popular_channels_by_category = dict()
        for user_category in user_categories:
            dict_of_popular_channels_by_category[user_category] = (
                list(self.category_to_telegram_channel[user_category]["channels"].items())[0: 100]
            )
        res = list()
        for i in range(50):
            for user_category in user_categories:
                channel_candidate = dict_of_popular_channels_by_category[user_category][i][0]
                if channel_candidate not in user_channels:
                    channel_score = dict_of_popular_channels_by_category[user_category][i][1]
                    res.append({
                        "id": channel_candidate,
                        "score": channel_score
                    })
        return res
