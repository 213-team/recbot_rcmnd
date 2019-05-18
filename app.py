from flask import Flask

from recbot_recsys.views.recommendations import popular_api
from recbot_recsys.popular_recommender import PopularRecommender


class RecSysBot(Flask):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.response_class.default_mimetype = "application/json"
        self.popular_recommender = None

    def init_recommender(self):
        self.popular_recommender = PopularRecommender()


def init_app(app: RecSysBot):
    app.register_blueprint(popular_api)
    app.init_recommender()


if __name__ == "__main__":
    app = RecSysBot(__name__)
    init_app(app)
    app.run(host="0.0.0.0", port=80)
