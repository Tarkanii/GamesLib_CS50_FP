from flask import Blueprint, redirect, request, render_template, make_response
from flask_login import login_required, current_user
from requests import get
import datetime
import math
import json
from . import db
from .models import Game
from sqlalchemy.exc import SQLAlchemyError
from . import MESSAGE_500, MESSAGE_404, API_KEY

main = Blueprint("main", __name__)
PLATFORMS_MAX = 5
GENRES_MAX = 3
PAGE_SIZE = 20.0

@main.route("/")
def index():
    return redirect("/games")

@main.route("/games")
def games():
    genres = []
    page = request.args.get("page") or 1
    search = request.args.get("search") or None
    genre = request.args.get("genres") or None

    if search and genre:
        url = get_url("games", { "search": search, "page_size": PAGE_SIZE, "page": page, "genres": genre })
    elif search and not genre:
        url = get_url("games", { "search": search, "page_size": PAGE_SIZE, "page": page })
    elif not search and genre:
        url = get_url("games", { "page_size": PAGE_SIZE, "page": page, "genres": genre })
    else:
        url = get_url("games", { "page_size": PAGE_SIZE, "page": page })

    genres_res = get(get_url("genres"))
    if genres_res.status_code == 200:
        data = genres_res.json()
        genres = data["results"]

    genre_name = None
    for genre_info in genres:
        if str(genre_info["id"]) == genre:
            genre_name = genre_info["name"]

    res = get(url)
    if res.status_code == 200:
        data = res.json()
        pagination = get_pagination(data["count"], PAGE_SIZE, page, search, genre)

        games = list(map(get_gamecard_info, data["results"]))
    elif res.status_code != 404:
        return render_template("error-page.html", user = current_user, message = MESSAGE_500)
    elif res.status_code == 404:
        return render_template("error-page.html", user = current_user, message = MESSAGE_404)

    return render_template("index.html", user = current_user, games = games, search = search, pagination = pagination, genre = genre_name, genres = genres)

@main.route("/games/<game_id>")
def game(game_id):
    res = get(get_url(f"games/{game_id}"))

    if res.status_code == 200:
        data = res.json()
    elif res.status_code != 404:
        return render_template("error-page.html", user = current_user, message = MESSAGE_500)
    elif res.status_code == 404:
        return render_template("error-page.html", user = current_user, message = MESSAGE_404)

    return render_template("game-page.html", user = current_user, game = get_game_content(data))

@main.route("/my-library")
@login_required
def my_library():
    games = []
    
    for game in current_user.games:
        res = get(get_url(f"games/{game}"))

        if res.status_code == 200:
            games.append(get_gamecard_info(res.json()))

    return render_template("my-library.html", user = current_user, games = games)

@main.route("/save-game", methods = ["POST"])
@login_required
def save_game():
    try:
        body = json.loads(request.data)
        id = body["id"]
    except: 
        return make_response({ "message": "Bad Request" }, 400)
    
    try:
        result = db.session.query(Game).filter(Game.game_id == int(id), Game.user_id == current_user.id)
        if len(list(result)) == 0:
            db.session.add(Game(int(id), current_user.id))
            db.session.commit()
    except SQLAlchemyError:
        return render_template("error-page.html", user = current_user, message = MESSAGE_500)

    return make_response({ "message": "Game saved" })

@main.route("/delete-game", methods = ["DELETE"])
@login_required
def delete_game():
    try:
        body = json.loads(request.data)
        id = body["id"]
    except: 
        return make_response({ "message": "Bad Request" }, 400)
    
    try:
        result = db.session.query(Game).filter(Game.game_id == int(id), Game.user_id == current_user.id)
        if len(list(result)) > 0:
            db.session.delete(result[0])
            db.session.commit()
        else:
            return make_response({ "message": "Game not found" }, 400)
    except SQLAlchemyError:
        return render_template("error-page.html", user = current_user, message = MESSAGE_500)
    
    return make_response({ "message": "Game deleted" }, 204)

def get_url(path, queries = {}):
    query_params = ""

    for key in queries:
        query_params += f"&{key}={queries[key]}"

    return f"https://api.rawg.io/api/{path}?key={API_KEY}{query_params}"

def get_pagination(count, page_size, current_page, search, genre):
    if count <= page_size:
        return None
    
    current_page = int(current_page)

    if search and genre:
        url = f"/games?search={search}&genres={genre}&page="
    elif search and not genre:
        url = f"/games?search={search}&page="
    elif not search and genre:
        url = f"/games?genres={genre}&page="
    else:
        url = "/games?page="

    max_page = math.ceil(count / page_size)
    pages_arr = []
    if max_page <= 5:
        i = 1
        while i <= max_page:
            pages_arr.append(str(i))
            i += 1

        return {
            "url": url,
            "max_page": str(max_page),
            "pages_arr": pages_arr,
            "current_page": str(current_page),
            "spaces": [False, False]
        }

    spaces = []
    if current_page - 1 >= 3 and max_page - current_page >= 3:
        spaces = [True, True]
        pages_arr = [1, current_page - 1, current_page, current_page + 1, max_page]
    elif current_page - 1 <= 3 and max_page - current_page >= 3:
        spaces = [False, True]
        i = 1
        while i <= 4:
            pages_arr.append(i)
            i += 1

        pages_arr.append(max_page)
    else:
        spaces = [True, False]
        pages_arr.append(1)
        i = max_page - 4
        while i <= max_page:
            pages_arr.append(i)
            i += 1

    pages_arr = [str(element) for element in pages_arr]
    return {
        "url": url,
        "max_page": str(max_page),
        "pages_arr": pages_arr,
        "current_page": str(current_page),
        "spaces": spaces
    }

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
        genres.append({ "name": genre["name"], "id": genre["id"] })
    
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
        genres.append({ "name": genre["name"], "id": genre["id"] })
    
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