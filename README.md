# Anime-List_recommender

Final Project for CS50P course
Created by Jody Bailey
[YouTube video for final project]()

## What Is This Project?

An anime list tracker and recommender command-line application written in python. It allows users to view, add, update, and delete entries for their own anime list, as well as recommend them new anime to watch

## Key Features

- Viewing current entries in their watch list
- Adding anime to their watch list by searching for the anime that matches the name provided
- Updating the status or score of the entries in their watch list
- Deleting watch list entries
- Getting a recommendation based on the criteria provided and the current entries in the watch list

## How it works

## Usage

Basic Usage
`python project.py <mode> <flags>`

Replace `<mode>` with one of the [valid modes](#modes) and replace `<flags>` with the appropriate flags available for each mode

### Modes

- `watchlist`
- `recommend`

### Watchlist Flags

- `-l --list`: List the current entries in the watch list
- `-a --add`: Add an entry into the watch list (**multi-step process**)
- `-u --update`: Update an entry in the watch list (**multi-step process**)
- `-d --delete`: Delete an entry in the watch list (**multi-step process**)

All flags that require a multi-step process will kick off an interactive terminal where you will provide input for the follow the steps for completing the process. For example, if you provide the `-a` flag, it will ask you to input the name of the anime, then call the graphql API with that name and provide you with the search results that best fit that name, then ask you which anime fits the name of the anime that was provided. This will continue until the last step of the process completes.

**NB**: Only one flag can be provided at a time for the `watchlist` mode

### Recommend Flags

- `-g --genres`: Genres that the anime should have (multiple values allowed)
- `-ms --min-score`: Minimum score that the anime should have
- `-me --max-episodes`: Maximum number of episodes that the anime can have
- `-f --format`: Format of the anime (multiple values allowed)
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

- Create a python virtual environment `python -m venv .venv` and activate the environment `source .venv/bin/activate` (The version used for developing the project was Python 3.12.2)
- Install dependencies `pip install -r requirements.txt`

To start the sqlite DB interactive terminal for debugging, run `sqlite3 anime.db`

## Directory structure

## References Used to Create Project
