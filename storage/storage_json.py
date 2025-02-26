import json
import os

class StorageJson:
    def __init__(self, filename="data/movies.json"):
        """
        Initialize the StorageJson object.
        Args:
            filename (str): The path of the JSON file to store movie data. Defaults to 'data/movies.json'.
        """
        self._filename = filename
        self._ensure_data_directory_exists()

    def _ensure_data_directory_exists(self):
        """Ensure that the 'data' directory exists."""
        directory = os.path.dirname(self._filename)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def list_movies(self):
        """Return the movies in the storage as a dictionary."""
        try:
            with open(self._filename, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            # Return an empty dictionary if the file doesn't exist or is empty
            return {}

    def add_movie(self, title, movie_data):
        """Add a new movie to the storage."""
        movies = self.list_movies()
        movies[title] = movie_data
        self._save_movies(movies)

    def delete_movie(self, title):
        """Delete a movie from the storage."""
        movies = self.list_movies()
        if title in movies:
            del movies[title]
            self._save_movies(movies)
            return True
        return False

    def update_movie(self, title, rating):
        """Update the rating of a movie."""
        movies = self.list_movies()
        if title in movies:
            movies[title]['rating'] = rating
            self._save_movies(movies)
            return True
        return False

    def _save_movies(self, movies):
        """Save the movie data to the JSON file."""
        try:
            with open(self._filename, 'w') as file:
                json.dump(movies, file, indent=4)
        except Exception as e:
            print(f"Error saving movies: {e}")
