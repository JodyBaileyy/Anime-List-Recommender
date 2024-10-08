# Anime-List_recommender

Final Project for CS50P course
Created by Jody Bailey
[YouTube video for final project]()

## What Is This Project?

An anime list tracker and recommender command-line application written in Python. It allows users to view, add, update, and delete entries for their own anime list, as well as recommend new anime to watch

## Key Features

- Viewing current entries in their watch list
- Adding anime to their watch list by searching for the anime that matches the name provided
- Updating the status or score of the entries in their watch list
- Deleting watch list entries
- Getting a recommendation based on the criteria provided and the current entries in the watch list

## How it works

It uses a single table in a SQLite database to hold all of the user's watch list entries. This database is created when you first run the application.

It utilizes [Anilist's GraphQL API](https://anilist.gitbook.io/anilist-apiv2-docs) for getting information about the entries in the user's watch list, as well as getting a recommendation based on the input given to the GraphQL query. This API requires no authentication and can be called by simply sending a request to the URL (<https://graphql.anilist.co>), with the specified query and query variables to get anime based on that criteria.

## Usage

Basic Usage:
`python project.py <mode> <flags>`

Example:
`python project.py watchlist -l`

Replace `<mode>` with one of the [valid modes](#modes) and replace `<flags>` with the appropriate flags available for each mode

### Modes

- `watchlist`
- `recommend`

### Watchlist Flags

- `-l --list`: List the current entries in the watch list
- `-a --add`: Add an entry into the watch list (**multi-step process**)
- `-u --update`: Update an entry in the watch list (**multi-step process**)
- `-d --delete`: Delete an entry in the watch list (**multi-step process**)

All flags that require a multi-step process will kick off an interactive terminal where you will provide input for the steps for completing the process. For example, if you provide the `-a` flag, it will ask you to input the name of the anime, then call the GraphQL API with that name and provide you with the search results that best fit that name, and then ask you which anime fits the name of the anime that was provided. This will continue until the last step of the process is completed.

**NB**: Only one flag can be provided at a time for the `watchlist` mode

### Recommend Flags

- `-g --genres`: Genres that the anime should have (**multiple values allowed**)
- `-ms --min-score`: Minimum score that the anime should have
- `-me --max-episodes`: Maximum number of episodes that the anime can have
- `-f --format`: Format of the anime (**multiple values allowed**)
- `-s --status`: Status of the anime

All valid values for the `genres`, `format`, or `status` flags are case-insensitive.

#### Valid Genres

- Action
- Adventure
- Comedy
- Drama,
- Ecchi
- Fantasy,
- Horror
- Mahou Shoujo
- Mecha
- Music
- Mystery
- Psychological
- Romance
- Sci-Fi
- Slice of Life
- Sports
- Supernatural
- Thriller

**NB** Ensure that double quotes (`""`) surround genres that contain multiple words. Example: `python project.py recommend -g "Mahou Shoujo" Sci-Fi "Slice of Life"`

#### Valid Formats

- TV
- TV_SHORT
- MOVIE
- SPECIAL
- OVA
- ONA
- MUSIC

#### Valid Statuses

- FINISHED
- RELEASING
- NOT_YET_RELEASED
- CANCELLED
- HIATUS

## Developer Guide

- Create a Python virtual environment `python -m venv .venv` and activate the environment `source .venv/bin/activate` (The version used for developing the project was Python 3.12.2)
- Install dependencies `pip install -r requirements.txt`

To start the SQLite DB interactive terminal for debugging, run `sqlite3 anime.db`

## Directory structure

### Queries

Contains the 2 GraphQL queries for getting a single anime and a list of anime, through pagination

#### .gitignore

All files/folders that should be ignored when pushing changes to github

#### constants

All static string variables

#### project

Contains the core functionality of the application, that is:

- The `main` method for setting up the command-line arguments and flags
- Several other methods for handling the core features, which are:
  - Viewing the entries in the user's watch list
  - Adding entries to the user's watch list
  - Updating entries in the user's watch list
  - Deleting entries in the user's watch list
  - Recommending a unique anime based on the criteria given and the current entries in the user's watch list

#### requirements

All pip installable dependencies required for this project to run.

#### sql_queries

All SQL queries that are utiliZed to interact with the SQLite database.

#### test_project

All 5 test classes for testing the 5 core features of the application

## References Used to Create Project

[Anilist GraphQL API](https://anilist.gitbook.io/anilist-apiv2-docs/docs)
[Official Python documentation on the argparse library](https://docs.python.org/3/library/argparse.html#choices)
[Official Python documentation on the unittestlibrary](https://docs.python.org/3/library/unittest.html#module-unittest)
