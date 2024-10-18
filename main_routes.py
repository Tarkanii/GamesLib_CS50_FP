from flask import Blueprint, request, make_response, render_template
from flask_login import login_required, current_user
from requests import get
import datetime

main = Blueprint("main", __name__)
PLATFORMS_MAX = 5
GENRES_MAX = 3

@main.route("/")
def index():
    res = get(get_url("games"))

    if res.status_code == 200:
        data = res.json()
        games = list(map(get_gamecard_info, data["results"]))

    return render_template("index.html", user = current_user, games = games)

@main.route("/my-library")
@login_required
def my_library():
    return render_template("my-library.html", user = current_user)

def get_url(path, queries = {}):
    query_params = ""

    for key in queries:
        query_params += f"&{key}={queries[key]}"

    return f"https://api.rawg.io/api/{path}?key=8ed35e34b6b447caa2701e9830460026{query_params}"

def get_gamecard_info(game):
    date = None
    diff = ""
    rating = None
    platforms = []
    genres = []
    metacritic_style = ""

    for platform in game["parent_platforms"]:
        if platform["platform"]["slug"] != "neo-geo" and platform["platform"]["slug"] != "3do":
            platforms.append(platform["platform"]["slug"])

    for genre in game["genres"]:
        genres.append(genre["name"])
    
    for game_rating in game["ratings"]: 
        if game_rating["id"] == game["rating_top"]:
            rating = game_rating["title"]

    if len(game["parent_platforms"]) - PLATFORMS_MAX > 0:
        diff = f"+{len(game["parent_platforms"]) - PLATFORMS_MAX}"

    if game["metacritic"]:
        if game["metacritic"] > 75:
            metacritic_style = "good"
        elif game["metacritic"] > 25:
            metacritic_style = "mid"
        else:
            metacritic_style = "bad"

    if game["released"]:
        date_split = game["released"].split("-")
        date = datetime.date(int(date_split[0]), int(date_split[1]), int(date_split[2])).strftime("%b %d, %Y")

    return {
        "title": game["name"] or "",
        "img": game["background_image"] or None,
        "platforms": platforms[:PLATFORMS_MAX],
        "diff": diff,
        "rating": rating,
        "metacritic": game["metacritic"] or None,
        "metacritic_style": metacritic_style,
        "released": date,
        "genres": genres[:GENRES_MAX]
    }