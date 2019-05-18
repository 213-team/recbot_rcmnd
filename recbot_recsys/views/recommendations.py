import json
from typing import Dict, List

from flask import Blueprint, current_app, request

popular_api = Blueprint("recommendations", __name__, url_prefix="/recommendations")


@popular_api.route("/popular/")
def get_channel_recommendations() -> Dict[str, List[str]]:
    """
    """
    channels = request.args.get("channels", type=str, default=None)
    channels_rec = current_app.popular_recommender.recommend(channels)

    return json.dumps({"res": channels_rec})
