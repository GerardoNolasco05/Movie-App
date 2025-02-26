import json
from typing import Dict


class StorageJson:
    def __init__(self, filename):
        self.filename = filename
        self.movies = self._load_movies()

    def _load_movies(self):
        try:
            with open(self.filename, mode='r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}  # If file is not found, return an empty dictionary

    def _save_movies(self):
        with open(self.filename, mode='w') as file:
            json.dump(self.movies, file, indent=4)

    def add_movie(self, title, movie_data):
        """
        Adds a movie to the storage.
        - title: The title of the movie (e.g., 'Titanic')
        - movie_data: Dictionary containing the movie details (rating, year, poster URL)
        """
        self.movies[title] = movie_data
        self._save_movies()

    def list_movies(self):
        return self.movies

    def delete_movie(self, title):
        if title in self.movies:
            del self.movies[title]
            self._save_movies()
            return True
        return False

    def update_movie(self, title, new_rating):
        if title in self.movies:
            self.movies[title]['rating'] = new_rating
            self._save_movies()
            return True
        return False