from sqlalchemy import create_engine, text
from sqlalchemy.exc import IntegrityError, OperationalError, ProgrammingError, DataError
import os

# absolute path to current file
current_file_path = os.path.abspath(__file__)
# path to the folder where the file is located
current_dir = os.path.dirname(current_file_path)
# path to the folder where the previous folder is located
project_root = os.path.dirname(current_dir)

db_path = os.path.join(project_root, "data", "movies.db")
DB_URL = f"sqlite:///{db_path}"

engine = create_engine(DB_URL)

with engine.connect() as connection:
    connection.execute(text("""
        CREATE TABLE IF NOT EXISTS movies (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE NOT NULL,
            year INTEGER NOT NULL,
            rating REAL NOT NULL,
            image TEXT
        )
    """))
    # save all changes
    connection.commit()


def list_movies():
    """Retrieve all movies from the database"""

    with engine.connect() as connection:
        try:
            result = connection.execute(text("SELECT title, year, rating,image FROM movies"))
            movies = result.fetchall()
            return movies

        except ProgrammingError as e:
            connection.rollback()
            print("SQL Programming Error:", e)
            return False

        except OperationalError:
            connection.rollback()
            print("Database connection error")
            return False


def add_movie(title: str, year: int, rating: float, image: str):
    """Add a new movie to the database"""

    with engine.connect() as connection:
        try:
            connection.execute(
                text("INSERT INTO movies (title, year, rating, image) VALUES (:title, :year, :rating, :image)"),
                {"title": title, "year": year, "rating": rating, "image": image})
            connection.commit()
            return True

        except IntegrityError:
            connection.rollback()
            print("Movie already exists (title must be unique)")
            return False

        except OperationalError:
            connection.rollback()
            print("Database connection error")
            return False

        except DataError:
            connection.rollback()
            print(f"Invalid data format")
            return False

        except ProgrammingError as e:
            connection.rollback()
            print("SQL Programming Error:", e)
            return False


def delete_movie(title: str):
    """Delete a movie from the database"""

    with engine.connect() as connection:
        try:
            connection.execute(text("DELETE FROM movies WHERE LOWER(title) = LOWER(:title)"),
                               {"title": title})
            connection.commit()
            return True

        except OperationalError:
            connection.rollback()
            print("Database connection error")
            return False

        except ProgrammingError as e:
            connection.rollback()
            print("SQL Programming Error:", e)
            return False


def update_movie(title: str, rating: float):
    """Update a movie's rating in the database"""

    with engine.connect() as connection:
        try:
            connection.execute(text("UPDATE movies SET rating = :rating WHERE LOWER(title) = LOWER(:title)"),
                               {"title": title, "rating": rating})
            connection.commit()
            return True

        except IntegrityError:
            connection.rollback()
            print("Failed to update the movie")
            return False

        except OperationalError:
            connection.rollback()
            print("Database connection error")
            return False

        except DataError:
            connection.rollback()
            print(f"Invalid data format")
            return False


print(list_movies())
