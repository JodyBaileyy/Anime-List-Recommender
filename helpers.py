import requests
import random
import re

from termcolor import colored
from tabulate import tabulate
from constants import URL
from sql_queries import watch_list_query

def paginated_response(query, variables):
    data = []
    page_num = 1

    first_response = requests.post(URL, json={"query": query, "variables": {
                                   "page": page_num, **variables}}).json()
    data.extend(first_response["data"]["Page"]["media"])

    has_next_page = first_response["data"]["Page"]["pageInfo"]["hasNextPage"]

    while has_next_page:
        page_num += 1
        response = requests.post(URL, json={"query": query, "variables": {
                                 "page": page_num, **variables}}).json()

        data.extend(response["data"]["Page"]["media"])
        has_next_page = response["data"]["Page"]["pageInfo"]["hasNextPage"]

    return data

def filter_out_watched_anime(db, all_anime):
    watch_list_anime_ids = [row[2] for row in db.execute(watch_list_query)]

    return list(filter(lambda anime: anime["id"] not in watch_list_anime_ids, all_anime))

def get_all_watch_list_anime(db):
    cursor = db.execute(watch_list_query)

    return [row for row in cursor]


def view_watch_list_simple(records):
    table_records = [table_record_for_viewing(
        index, row) for index, row in enumerate(records)]
    table_headers = ["", "Name", "Status", "Score"]

    print(tabulate(table_records, headers=table_headers,
          tablefmt="presto"), end="\n\n")


def get_single_anime(id):
    with open('./queries/media.graphql', 'r') as file:
        query = file.read()

    response = requests.post(
        URL, json={"query": query, "variables": {"id": id}}).json()

    return response["data"]["Media"]

def formatted_score(score):
    result = "⭐️"

    if not score:
        result += colored("_", "red")
    elif 0 <= int(score) < 50:
        result += colored(score, "red")
    elif 50 <= int(score) < 70:
        result += colored(score, "yellow")
    elif 70 <= int(score) < 80:
        result += colored(score, "light_green")
    else:
        result += colored(score, "green")

    return result

def format_response_for_add(index, record):
    title = get_anime_title(record["title"])
    score = record["averageScore"]
    year = record["startDate"]["year"] or "unreleased"

    return [index + 1, title, formatted_score(score), year]


def get_anime_title(title_object):
    return title_object["english"] or title_object["userPreferred"]


def formatted_recommended_anime(anime):
    title = get_anime_title(anime["title"])
    score = formatted_score(anime["averageScore"])
    episodes = anime["episodes"]
    format = anime["format"]
    genres = ", ".join(anime["genres"])
    released = f"{anime["season"]} {anime["startDate"]["year"]}"
    studio = anime["studios"]["edges"][0]["node"]["name"]
    synopsis = re.sub(r"</?\w+>", "", anime["description"])
    trailer = get_trailer_link(anime["trailer"])

    return (
        f"""
{colored('TITLE', 'light_blue')}: {title}
{colored('SCORE', 'light_green')}: {score}
{colored('EPISODES', 'light_yellow')}: {episodes}
{colored('FORMAT', 'light_blue')}: {format}
{colored('GENRES', 'light_green')}: {genres}
{colored('RELEASED', 'light_yellow')}: {released}
{colored('STUDIO', 'light_blue')}: {studio}

{colored('SYNOPSIS', 'light_green')}: {synopsis}

{colored('TRAILER', 'light_yellow')}: {trailer}
    """
    )
    

def get_trailer_link(trailer_object):
    if not trailer_object:
        return "No trailer published"

    if trailer_object["site"] == "youtube":
        return f"https://www.youtube.com/watch?v={trailer_object['id']}"
    elif trailer_object["site"] == "dailymotion":
        return f"https://www.dailymotion.com/video/{trailer_object['id']}"
    

def get_random_anime(list_of_anime):
    random_index = random.randint(0, len(list_of_anime) - 1)

    return list_of_anime[random_index]


def format_record_for_watch_list(anime, anime_details, index):
    return [
        index,
        anime[1],
        formatted_status(anime[4]),
        formatted_score(anime[3]),
        anime_details["format"],
        anime_details["episodes"],
        anime_details["startDate"]["year"] or "unreleased",
        anime_details["season"],
        anime_details["studios"]["edges"][0]["node"]["name"]
    ]


def formatted_status(status):
    match status:
        case "COMPLETED":
            return f"✅{colored(status.lower(), 'green')}"
        case "ON HOLD":
            return f"🟠{colored(status.lower(), 'light_yellow')}"
        case "PLAN TO WATCH":
            return f"📖{colored(status.lower(), 'light_cyan')}"
        case "DROPPED":
            return f"🚮{colored(status.lower(), 'red')}"
        case "WATCHING":
            return f"👀{colored(status.lower(), 'light_blue')}"
        
def table_record_for_viewing(index, row):
    return [index + 1, row[1], formatted_status(row[4]), formatted_score(row[3])]