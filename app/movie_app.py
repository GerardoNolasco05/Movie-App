import requests
import statistics
import random
from difflib import get_close_matches
import os
from dotenv import load_dotenv



class MovieApp:
    def __init__(self, storage):
        """
        Initialize the MovieApp with a storage mechanism (e.g., CSV, JSON).
        """
        self._storage = storage

    def _command_list_movies(self):
        """
        Lists all movies from the storage and displays the total count.
        """
        movies = self._storage.list_movies()
        movie_count = len(movies)  # Count total movies

        if movie_count > 0:
            print(f"\n{movie_count} movies in total")
            for title, details in movies.items():
                print(f"{title} ({details['year']}), Rating: {details['rating']}")
        else:
            print("No movies found in your collection.")

    def _command_add_movie(self):
        """
        Adds a movie to the storage by fetching its details (Title, Year, Rating, Poster Image URL)
        from the OMDb API, based on the movie title entered by the user.
        """
        movie_title = input("Enter new movie name: ")

        # Load environment variables from the .env file in the parent directory
        load_dotenv(os.path.join(os.path.dirname(__file__), '.env'))
        # Make the API request to fetch movie details
        api_key = os.getenv("OMDB_API_KEY")  # Securely get API key from environment variable
        url = f"http://www.omdbapi.com/?apikey={api_key}&t={movie_title}"

        try:
            # Sending the request to the OMDb API
            response = requests.get(url)

            # Check if the response is successful
            if response.status_code == 200:
                data = response.json()

                if data["Response"] == "True":
                    # Movie found, extracting details
                    title = data["Title"]
                    year = data["Year"]
                    # IMDb rating, might not be available for all movies
                    rating = data.get("imdbRating", "N/A")
                    # Poster image URL, might not be available for all movies
                    poster_url = data.get("Poster", "N/A")
                    # Save the movie to the storage
                    movie_data = {
                        "rating": rating,
                        "year": year,
                        "poster": poster_url
                    }

                    self._storage.add_movie(title, movie_data)
                    print(f"Movie {title} successfully added")

                else:
                    # Movie not found in the API
                    print(f"Didn't find movie {movie_title} in the API.")
            else:
                # If the response code is not 200, handle the unexpected error
                print(f"Error: Failed to fetch data. Server responded with status code {response.status_code}")

        except requests.exceptions.RequestException as e:
            # Handle any network errors (e.g., no internet connection, DNS resolution error)
            print("Error: Failed to connect to the OMDb API. Please check your internet connection or try again later.")
            print("Details:", e)

    def _command_delete_movie(self):
        """
        Deletes a movie from the storage based on the movie title.
        """
        movie_title = input("Enter movie name to delete: ")
        if self._storage.delete_movie(movie_title):
            print(f"Movie '{movie_title}' successfully deleted")
        else:
            print(f"Movie {movie_title} doesn't exist!")

    def _command_update_movie(self):
        """
        Updates the movie rating in the storage based on the movie title.
        """
        movie_title = input("Enter movie title to update: ")
        new_rating = input("Enter new rating (0-10): ")
        if self._storage.update_movie(movie_title, new_rating):
            print(f"Movie '{movie_title}' rating updated to {new_rating}.")
        else:
            print(f"Error: Movie '{movie_title}' not found.")

    def _command_movie_stats(self):
        """
        Displays statistics about the movie collection, including:
        - Average rating
        - Median rating
        - Best movie
        - Worst movie
        """
        movies = self._storage.list_movies()

        if not movies:
            print("No movies found in your collection.")
            return

        ratings = []
        for title, details in movies.items():
            try:
                rating = float(details["rating"])
                ratings.append((rating, title))  # Store as (rating, title) for sorting
            except ValueError:
                continue  # Skip movies with invalid or missing ratings

        if not ratings:
            print("No valid ratings found.")
            return

        ratings.sort()  # Sort by rating
        avg_rating = sum(r[0] for r in ratings) / len(ratings)
        median_rating = statistics.median(r[0] for r in ratings)
        best_movie = ratings[-1]  # Last item (highest rating)
        worst_movie = ratings[0]  # First item (lowest rating)

        print("\nMovie Statistics:")
        print(f"Average rating: {avg_rating:.2f}")
        print(f"Median rating: {median_rating:.2f}")
        print(f"Best movie: {best_movie[1]} ({best_movie[0]})")
        print(f"Worst movie: {worst_movie[1]} ({worst_movie[0]})")

    def _command_random_movie(self) -> None:
        """Private method to get a random movie."""
        movies = self._storage.list_movies()
        if not movies:
            print("No movies in the database.")
        else:
            movie = random.choice(list(movies.keys()))
            print(f"Your movie for tonight: {movie}, it's rated {movies[movie]['rating']}")

    def _command_search_movie(self) -> None:
        """Private method to search for a movie."""
        search_query = input("Enter part of movie name: ").lower()
        movies = self._storage.list_movies()
        matches = {movie: details for movie, details in movies.items() if search_query in movie.lower()}

        if matches:
            for movie, details in matches.items():
                print(f"{movie}, {details['rating']}")
        else:
            similar_movies = get_close_matches(search_query, movies.keys(), n=3, cutoff=0.6)
            if similar_movies:
                print("Did you mean:")
                for sm in similar_movies:
                    print(f"- {sm}: {movies[sm]['rating']}")
            else:
                print("No similar movies found.")

    def _command_movies_sorted_rating(self) -> None:
        """Lists movies sorted by rating (highest to lowest)."""
        movies = self._storage.list_movies()

        if not movies:
            print("No movies found in your collection.")
            return

        # Convert ratings to float and handle missing values
        sorted_movies = sorted(
            movies.items(),
            key=lambda item: float(item[1]['rating']) if item[1]['rating'] != "N/A" else 0,
            reverse=True
        )

        print("\nMovies sorted by rating:")
        for movie, details in sorted_movies:
            print(f"{movie}: {details['rating']}")

    def _command_generate_website(self):
        """Generates and saves a webpage based on the movie collection."""
        try:
            # Open the template file from the 'static' directory with explicit encoding
            with open('static/index_template.html', 'r', encoding='utf-8') as template_file:
                template_content = template_file.read()

            # Create the movie grid HTML based on the movie collection
            movies = self._storage.list_movies()
            movie_grid = ""

            for title, details in movies.items():
                movie_item = f'''
                    <li class="movie">
                        <img class="movie-poster" src="{details['poster']}" alt="{title} poster"/>
                        <div class="movie-title">{title}</div>
                        <div class="movie-year">{details['year']}</div>
                    </li>
                '''
                movie_grid += movie_item

            # Replace the placeholders in the template
            webpage_content = template_content.replace("__TEMPLATE_TITLE__", "My Movie App")
            webpage_content = webpage_content.replace("__TEMPLATE_MOVIE_GRID__", movie_grid)

            # Save the generated HTML content in the 'static' directory
            with open('static/index.html', 'w') as output_file:
                output_file.write(webpage_content)

            print("Website was generated successfully.")

        except FileNotFoundError:
            print("Error: Template file not found in the 'static' directory.")
        except Exception as e:
            print(f"Error generating website: {e}")

    def display_menu(self):
        """
        Displays the main menu for user interaction.
        """
        print("\nMenu:")
        print("0. Exit")
        print("1. List Movies")
        print("2. Add Movie")
        print("3. Delete Movie")
        print("4. Update Movie")
        print("5. Stats")
        print("6. Random movie")
        print("7. Search movie")
        print("8. Movies sorted by rating")
        print("9. Generate Website")

    def run(self):
        """
        Starts the movie app and runs the main loop for user interaction.
        """
        while True:
            self.display_menu()
            choice = input("Enter your choice (0-9): ")

            if choice == "1":
                self._command_list_movies()
            elif choice == "2":
                self._command_add_movie()
            elif choice == "3":
                self._command_delete_movie()
            elif choice == "4":
                self._command_update_movie()
            elif choice == "5":
                self._command_movie_stats()
            elif choice == "6":
                self._command_random_movie()
            elif choice == "7":
                self._command_search_movie()
            elif choice == "8":
                self._command_movies_sorted_rating()
            elif choice == "9":
                self._command_generate_website()
            elif choice == "0":
                print("Bye!")
                break
            else:
                print("Invalid choice")

            input("\nPress Enter to continue")

