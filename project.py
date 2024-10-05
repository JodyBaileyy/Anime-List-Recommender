import sqlite3
import argparse


from tabulate import tabulate
from sql_queries import create_table_query, add_anime_query, watch_list_query, update_query, delete_query
from constants import VALID_FORMATS, VALID_GENRES, VALID_PROPERTIES, VALID_STATUSES, VALID_MEDIA_STATUSES
from helpers import (
    get_single_anime,
    paginated_response,
    format_response_for_add,
    get_anime_title,
    formatted_recommended_anime,
    get_random_anime,
    format_record_for_watch_list,
    table_record_for_viewing
)


def main():
    conn = sqlite3.connect("anime.db")
    conn.execute(create_table_query)
    parser = argparse.ArgumentParser(
        prog="WatchListRecommender", description="Add / Update your own anime watch list & reccommend new anime to watch")
    parser.add_argument("mode", choices=[
                        "watchlist", "recommend"], help="The feature mode you'd like to access", metavar="mode")
    parser.add_argument("-l", "--list", action="store_true",
                        help="watchlist: view your currentl watch list")
    parser.add_argument("-a", "--add", action="store_true",
                        help="watchlist: kicks off process to add an anime to your watchlist")
    parser.add_argument("-u", "--update", action="store_true",
                        help="watchlist: kicks off process to update an entry in your watchlist")
    parser.add_argument("-d", "--delete", action="store_true",
                        help="watchlist: kicks off process to delete and entry in your watchlist")
    parser.add_argument("-g", "--genres", action="extend", nargs="*", choices=VALID_GENRES,
                        type=str.title, help="recommend: the genres for the anime")
    parser.add_argument("-ms", "--min-score", action="store", nargs="?",
                        type=int, help="recommend: the minimum scorevof the anime (1-100)")
    parser.add_argument("-me", "--max-episodes", action="store", nargs="?", type=int,
                        help="recommend: the maximum amount of episode the anime is allowed to have")
    parser.add_argument("-f", "--formats", action="extend", nargs="*", choices=VALID_FORMATS,
                        type=str.upper, help="recommend: the media formats for the anime")
    parser.add_argument("-s", "--status", action="store", nargs="?", type=str.upper, choices=VALID_MEDIA_STATUSES,
                        help="recommend: the status of the anime")

    args = parser.parse_args()

    match args.mode:
        case "watchlist":
            handle_watch_list(conn, args)
        case "recommend":
            handle_recommend(conn, args)

    conn.close()


def handle_recommend(db, args):
    if args.list or args.update or args.add or args.delete:
        invalid_flag_msg = "A watchlist flag was provided for the recommend mode. Valid recommend mode flags: ['-g', '--genres', '-ms', '--min-score', '-me', '--max-episodes', '-f', '--formats', '-s', '--status']"
        return print(invalid_flag_msg)
    get_recommended_anime(
        db=db,
        genres=args.genres,
        min_score=args.min_score,
        max_episodes=args.max_episodes,
        formats=args.formats,
        status=args.status
    )


def handle_watch_list(db, args):
    if args.genres or args.formats or args.status or args.min_score or args.max_episodes:
        invalid_flag_msg = "A recommend flag was provided for the watchlist mode. Valid watchlist mode flags: ['-l', '--list', '-a', '--add', '-u', '--update', '-d', '--delete']"
        return print(invalid_flag_msg)

    if args.list:
        view_watch_list(db)
    elif args.add:
        add_anime_to_watch_list(db)
    elif args.update:
        update_anime_in_watch_list(db)
    elif args.delete:
        delete_anime_in_watch_list(db)


def get_recommended_anime(db, genres, min_score, max_episodes, formats, status):
    variables = {
        "genre_in": genres,
        "averageScore_greater": min_score,
        "episodes_lesser": max_episodes,
        "format_in": formats or ["TV"],
        "status": status or "FINISHED"
    }

    filtered_variables = {key: value for key,
                          value in variables.items() if value}

    with open("./queries/media_pages.graphql") as file:
        query = file.read()

    response = paginated_response(query, filtered_variables)

    if len(response) == 0:
        return print("No anime found with current options. Try narrowing down the criteria given")

    filtered_response = filter_out_watched_anime(db, response)

    if len(filtered_response) == 0:
        return print("All anime that match the given criteria are included in your watch list")

    random_anime = get_random_anime(filtered_response)
    recommended_anime = formatted_recommended_anime(random_anime)
    print(recommended_anime)

    while True:
        add_answer = input("Add anime to your watch list? ").strip().lower()

        if add_answer in ["y", "yes"]:
            db.execute(add_anime_query, (random_anime["id"], get_anime_title(
                random_anime["title"]), None, "PLAN TO WATCH"))
            db.commit()

            return print(f"Added {get_anime_title(random_anime["title"])} to your watch list")
        elif add_answer in ["n", "no"]:
            return
        else:
            print(
                "Invalid option given. Valid options: ['y', 'yes', 'n', 'no']")


def filter_out_watched_anime(db, all_anime):
    watch_list_anime_ids = [row[2] for row in db.execute(watch_list_query)]

    return list(filter(lambda anime: anime["id"] not in watch_list_anime_ids, all_anime))


def delete_anime_in_watch_list(db):
    anime = get_all_watch_list_anime(db)

    if len(anime) == 0:
        return print("No watch list entries to delete")
    
    view_watch_list_simple(anime)

    while True:
        error_msg = "Please provide a valid option"

        try:
            anime_num = int(
                input("Which of the following entries would you like to delete? ").strip())

            if anime_num > len(anime) or anime_num <= 0:
                print(error_msg)
                continue

            break
        except ValueError:
            print(error_msg)

    while True:
        entry_to_delete = anime[anime_num - 1]
        anime_name = entry_to_delete[1]

        confirmed_response = input(f"Are you sure you want to delete your entry for {
                                   anime_name}? ").lower()

        if confirmed_response in ["y", "yes"]:
            db.execute(delete_query, [str(entry_to_delete[0])])
            db.commit()

            print(f"Successfully deleted {anime_name} from your watch list")
            break
        elif confirmed_response in ["n", "no"]:
            print(f"Cancelling delete process")
            break
        else:
            print("Invalid response given. Cancelling delete process")
            break


def view_watch_list(db):
    cursor = db.execute(watch_list_query)
    anime = [row for row in cursor]

    if len(anime) == 0:
        return print("Watchlist is currently empty")

    anime_details = [get_single_anime(row[2]) for row in anime]
    table_headers = ["", "Name", "Status", "Score",
                     "Type", "Episodes", "Released", "Season", "Studio"]
    table_records = [
        format_record_for_watch_list(record, anime_details[index], index)
        for index, record in enumerate(anime)
    ]

    print(tabulate(table_records, headers=table_headers, tablefmt="presto"))


def get_all_watch_list_anime(db):
    cursor = db.execute(watch_list_query)
    
    return [row for row in cursor]


def view_watch_list_simple(records):
    table_records = [table_record_for_viewing(index, row) for index, row in enumerate(records)]
    table_headers = ["", "Name", "Status", "Score"]
    
    print(tabulate(table_records, headers=table_headers,
          tablefmt="presto"), end="\n\n")
    

def update_anime_in_watch_list(db):
    anime = get_all_watch_list_anime(db)

    if len(anime) == 0:
        return print("No watch list entries to update")
    
    view_watch_list_simple(anime)

    while True:
        error_msg = "Please provide a valid option"

        try:
            anime_num = int(
                input("Which of the following entries would you like to update? ").strip())

            if anime_num > len(anime) or anime_num <= 0:
                print(error_msg)
                continue

            break
        except ValueError:
            print(error_msg)

    while True:
        column = input(
            "What property would you like to update? ").strip().upper()

        if column not in VALID_PROPERTIES:
            print(
                f"Invalid property provided. Valid Properties: {list(map(lambda property: property.lower(), VALID_PROPERTIES))}")
            continue

        break

    while True:
        new_value = input(f"New value for {column.lower()}: ").strip()

        match column:
            case "STATUS":
                new_value = new_value.upper()

                if new_value not in VALID_STATUSES:
                    print(
                        f"Invalid status provided. Valid statuses: {list(map(lambda status: status.lower(), VALID_STATUSES))}")
                    continue
            case "SCORE":
                error_msg = "Invalid Score Provided"

                try:
                    new_value = int(new_value)

                    if new_value > 100 or new_value < 0:
                        print(error_msg)
                        continue
                except ValueError:
                    print(error_msg)

        break

    print()

    anime_to_update = anime[anime_num - 1]

    db.execute(update_query.format(column=column.lower()),
               (new_value, anime_to_update[0]))
    db.commit()

    print(
        f"Successfully updated {anime_to_update[1]}'s {column.lower()} to {new_value}")


def add_anime_to_watch_list(db):
    with open("./queries/media_pages.graphql", "r") as file:
        query = file.read()

    while True:
        name = input("What is the name of the anime? ").strip()

        variables = {"search": name}
        records = paginated_response(query, variables)

        if len(records) == 0:
            print(f"No anime found with name {name}")
            continue

        table_headers = ["", "Name", "Score", "Release Date"]
        table_records = [
            format_response_for_add(index, record)
            for index, record in enumerate(records)
        ]

        print(tabulate(table_records, headers=table_headers,
              tablefmt="presto"), end="\n\n")
        break

    while True:
        error_msg = "Please provide a valid option"

        try:
            anime_index = int(input(
                f"Which of the following matches the anime {name}? ").strip())

            if anime_index <= 0 or anime_index > len(records):
                print(error_msg)
                continue

            break
        except ValueError:
            print(error_msg)

    while True:
        status = input(
            f"What status would you like to give this anime? ").strip().upper()

        if status in VALID_STATUSES:
            break

        print(
            f"Invalid status provided. Valid statuses: {list(map(lambda status: status.lower(), VALID_STATUSES))}")

    while True:
        error_msg = "Invalid Score Provided"\

        try:
            score = int(
                input('Score of anime from 1 - 100 (optional. Press crtl + d to skip): ').strip())

            if score > 100 or score < 0:
                print(error_msg)
            else:
                break
        except ValueError:
            print(error_msg)
        except EOFError:
            score = None
            break

    print()

    anime = records[anime_index - 1]
    media_id = anime["id"]
    title = get_anime_title(anime["title"])

    db.execute(add_anime_query, (media_id, title, score, status))
    db.commit()

    print(f"Added {title} to watch list")


if __name__ == "__main__":
    main()
