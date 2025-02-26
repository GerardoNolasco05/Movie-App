from abc import ABC, abstractmethod


class IStorage(ABC):
    """
    Interface for movie storage systems.
    Defines the required methods for managing movie data.
    """

    @abstractmethod
    def list_movies(self):
        """Retrieve a dictionary of all movies stored."""
        pass

    @abstractmethod
    def add_movie(self, title, year, rating, poster):
        """Add a new movie with title, year, rating, and poster URL."""
        pass

    @abstractmethod
    def delete_movie(self, title):
        """Remove a movie from the storage by title."""
        pass

    @abstractmethod
    def update_movie(self, title, rating):
        """Update the rating of an existing movie."""
        pass


