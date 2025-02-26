from app.movie_app import MovieApp
from storage.storage_csv import StorageJson

def main():
    # Choose storage type (JSON or CSV)
    storage = StorageJson('data/movies.json')  # or StorageCsv('movies.csv')
    movie_app = MovieApp(storage)
    movie_app.run()

if __name__ == "__main__":
    main()