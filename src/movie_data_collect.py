import requests
import json
import os

API_KEY = ""
BASE = "https://api.themoviedb.org/3"

def searchMovieId(movie):
    response = requests.get(f"{BASE}/search/movie",
                            params={"api_key": API_KEY, "query": movie})
    
    if (response.status_code == 200):
        data = response.json()
        id = data["results"][0]['id']
        print(id)
        return
    
    # non 200 status code
    raise Exception(f"ID search not successful: {response.status_code}")
        
        
searchMovieId("Babylon")
