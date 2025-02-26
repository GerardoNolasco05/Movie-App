from movie_app import MovieApp
from storage_json import StorageJson  # or from storage_csv import StorageCsv

def main():
    # Choose storage type (JSON or CSV)
    storage = StorageJson('movies.json')  # or StorageCsv('movies.csv')
    movie_app = MovieApp(storage)
    movie_app.run()

if __name__ == "__main__":
    main()