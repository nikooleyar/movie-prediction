# Niko Oleyar
# 10/26/26
# Export movie data gathered from TheMovieDB for each entry in 
# a list of letterboxd ratings

import csv
import json
import requests
from pathlib import Path

API_KEY = ""
BASE = "https://api.themoviedb.org/3"
DIRECTORY = Path(__file__).resolve().parent.parent  # twice for one level above /src
DATA_FILE = DIRECTORY / "data" / "movie_data.json"


def searchMovieId(movie, year):
    response = requests.get(f"{BASE}/search/movie",
                            params={"api_key": API_KEY, "query": movie, "year": year})
    if (response.status_code != 200):
        # non 200 status code
        raise Exception(f"ID search not successful: {response.status_code}")
    data = response.json()
    return data["results"][0]['id']
        
        
def fetchDetails(id):
    response = requests.get(f"{BASE}/movie/{id}",
                           params={"api_key": API_KEY,
                            "append_to_response": "credits,keywords,release_dates"})
                            #includes cast, community keywords, etc
    if (response.status_code != 200):
        raise Exception(f"Details could not be fetched: {response.status_code}")
    return response.json()


def exportData(movie):
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "a") as f:
        f.write(json.dumps(movie) + "\n")
    print(f"Saved {movie['title']} to {DATA_FILE}")


def fetchMovieList(path):
    with open(path) as f:
        # use the provided year to get the right movie
        return [(row["Name"], row["Year"], float(row["Rating"])) for row in csv.DictReader(f)]


for title, year, rating in fetchMovieList(DIRECTORY / "letterboxd_export" / "ratings.csv"):
    try:
        movie = fetchDetails(searchMovieId(title, year))
        movie["my_rating"] = rating
        exportData(movie)
    except Exception as e:
        print(f"Skipped {title}: {e}")  # didn't work, but continue
