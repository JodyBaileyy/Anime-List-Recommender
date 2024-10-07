VALID_STATUSES = [
    "COMPLETED",
    "ON HOLD",
    "PLAN TO WATCH",
    "DROPPED",
    "WATCHING"
]

VALID_PROPERTIES = [
    "SCORE",
    "STATUS"
]

VALID_MEDIA_STATUSES = [
    "FINISHED",
    "RELEASING",
    "NOT_YET_RELEASED",
    "CANCELLED",
    "HIATUS"
]

VALID_GENRES = [
    "Action",
    "Adventure",
    "Comedy",
    "Drama",
    "Ecchi",
    "Fantasy",
    "Horror",
    "Mahou Shoujo",
    "Mecha",
    "Music",
    "Mystery",
    "Psychological",
    "Romance",
    "Sci-Fi",
    "Slice of Life",
    "Sports",
    "Supernatural",
    "Thriller"
]

VALID_FORMATS = [
    "TV",
    "TV_SHORT",
    "MOVIE",
    "SPECIAL",
    "OVA",
    "ONA",
    "MUSIC"
]

URL = 'https://graphql.anilist.co'

WATCH_LIST_EMPTY_MSG = "Watchlist is currently empty"
MULTIPLE_FLAGS_ERR_MSG = "Multiple flags added for the watchlist mode. Only one flag is allowed"
NO_RECOMMENDATIONS_FOUND_MSG = "No anime found with current options. Try narrowing down the criteria given"
NO_UNIQUE_RECOMMENDATION_FOUND_MSG = "All anime that match the given criteria are included in your watch list"
CANCEL_DELETE_MSG = "Cancelling delete process"

INVALID_SCORE_MSG = "Invalid Score Provided"
INVALID_OPTION_MSG = "Please provide a valid option"
INVALID_CONFIRMATION_MSG = "Invalid response given. Valid responses: ['y', 'yes', 'n', 'no']"
INVALID_WATCH_LIST_FLAG_MSG = "A recommend flag was provided for the watchlist mode. Valid watchlist mode flags: ['-l', '--list', '-a', '--add', '-u', '--update', '-d', '--delete']"
INVALID_RECOMMEND_FLAG_MSG = "A watchlist flag was provided for the recommend mode. Valid recommend mode flags: ['-g', '--genres', '-ms', '--min-score', '-me', '--max-episodes', '-f', '--formats', '-s', '--status']"
INVALID_PROPERTIES_MSG = f"Invalid property provided. Valid Properties: {list(map(lambda property: property.lower(), VALID_PROPERTIES))}"
INVALID_STATUS_MSG = f"Invalid status provided. Valid statuses: {list(map(lambda status: status.lower(), VALID_STATUSES))}"