from flask import Blueprint, redirect, request, make_response, render_template
from flask_login import login_required, current_user
from requests import get
import datetime

main = Blueprint("main", __name__)
PLATFORMS_MAX = 5
GENRES_MAX = 2

@main.route("/")
def index():
    return redirect("/games")

@main.route("/games")
def games():
    search = request.args.get("search")
    if search:
        url = get_url("games", { "search": search })
    else:
        url = get_url("games")

    res = get(url)
    if res.status_code == 200:
        data = res.json()
        games = list(map(get_gamecard_info, data["results"]))

    return render_template("index.html", user = current_user, games = games, search = search)

@main.route("/games/<game_id>")
def game(game_id):
    res = get(get_url(f"games/{game_id}"))

    if res.status_code == 200:
        data = res.json()

    return render_template("game-page.html", user = current_user, game = get_game_content(data))

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

    if "parent_platforms" in game:
        for platform in game["parent_platforms"]:
            if platform["platform"]["slug"] != "neo-geo" and platform["platform"]["slug"] != "3do":
                platforms.append(platform["platform"]["slug"])

    for genre in game["genres"]:
        genres.append(genre["name"])
    
    for game_rating in game["ratings"]: 
        if game_rating["id"] == game["rating_top"]:
            rating = game_rating["title"]

    if "parent_platforms" in game and len(game["parent_platforms"]) - PLATFORMS_MAX > 0:
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
        "id": game["id"],
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

def get_game_content(game):
    date = None
    parent_platforms = []
    platforms = []
    genres = []
    developers = []
    publishers = []
    metacritic_style = ""
    top_rating = ""
    bar_ratings = { 
        "exceptional": {
            "count": "",
            "percent": 0
        },
        "recommended": {
            "count": "",
            "percent": 0
        },
        "meh": {
            "count": "",
            "percent": 0
        },
        "skip": {
            "count": "",
            "percent": 0
        },
    }

    for platform in game["parent_platforms"]:
        if platform["platform"]["slug"] != "neo-geo" and platform["platform"]["slug"] != "3do":
            parent_platforms.append(platform["platform"]["slug"])

    for platform in game["platforms"]:    
        platforms.append(platform["platform"]["name"])

    for genre in game["genres"]:
        genres.append(genre["name"])
    
    for developer in game["developers"]:
        developers.append(developer["name"])

    for publisher in game["publishers"]:
        publishers.append(publisher["name"])

    if game["metacritic"]:
        if game["metacritic"] > 75:
            metacritic_style = "good"
        elif game["metacritic"] > 25:
            metacritic_style = "mid"
        else:
            metacritic_style = "bad"

    for rating in game["ratings"]: 
        if rating["id"] == game["rating_top"]:
            top_rating = rating["title"]

    for rating in game["ratings"]: 
        bar_ratings[rating["title"]]["count"] = rating["count"]
        bar_ratings[rating["title"]]["percent"] = rating["percent"]

    if game["released"]:
        date_split = game["released"].split("-")
        date = datetime.date(int(date_split[0]), int(date_split[1]), int(date_split[2])).strftime("%b %d, %Y")

    return {
        "id": game["id"],
        "title": game["name"] or "",
        "bg": game["background_image"] or None,
        "parent_platforms": parent_platforms,
        "platforms": platforms,
        "top_rating": top_rating,
        "ratings": game["ratings"],
        "ratings_count": game["ratings_count"],
        "metacritic": game["metacritic"] or None,
        "metacritic_style": metacritic_style,
        "released": date,
        "genres": genres,
        "developers": developers,
        "publishers": publishers,
        "playtime": game["playtime"] or None,
        "bar_ratings": bar_ratings,
        "description": game["description_raw"] or "",
        "website": game["website"] or ""
    }