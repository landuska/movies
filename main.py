import random
import statistics
import matplotlib.pyplot as plt
from colorama import init, Fore
from movie_storage import movie_storage_sql as storage
import api_movies as api
import generate_web as web

init()


def is_movie_in_db(title: str, movies: list):
    """
        Check if a movie with the given title already exists in the database.

        Args:
            title (str): The title of the movie to check.
            movies (list): List of movies, each as a tuple (title, year, rating, image).

        Returns:
            bool: True if the movie exists, False otherwise.
        """
    for movie in movies:
        if movie[0].lower() == title.lower():
            return True

    return False


def get_user_input():
    """
    Prompt the user to enter a movie title and validate it is not empty.

    Returns:
        str: The movie title entered by the user.
    """

    while True:
        user_input_title = api.normalize(input(Fore.GREEN + "Please enter the movie title: ")).strip()

        if user_input_title:
            return user_input_title
        else:
            print(Fore.RED + "Please enter a title, not an empty string")


def print_menu_and_select_from_the_main_menu():
    """
    Print the main menu and prompt the user to select an option.

    Returns:
        str: The option selected by the user.
    """

    select_from_the_main_menu = input(Fore.YELLOW +
                                      "Menu:\n"
                                      "0. Exit\n"
                                      "1. List movies\n"
                                      "2. Add movie\n"
                                      "3. Update movie\n"
                                      "4. Delete movie\n"
                                      "5. Stats\n"
                                      "6. Random movie\n"
                                      "7. Search movie\n"
                                      "8. Movies sorted by rating\n"
                                      "9. Histograma\n"
                                      "10. Website\n\n"
                                      "Enter choice (0-10): ").strip()
    return select_from_the_main_menu


def command_list_movies(movies: list):
    """
    Print all movies from the database with their title, year, and rating.

    Args:
        movies (list): List of movies, each as a tuple (title, year, rating, image).

    Returns:
        None
    """

    print(Fore.WHITE + f"{'*' * 20} {len(movies)} movies in total {'*' * 20}")

    for movie in movies:
        title = movie[0]
        rating = movie[2]
        year = movie[1]
        print(Fore.WHITE + f"{title}, rating: {rating}, year: {year}")

    print(Fore.WHITE + f"{'*' * 60}")


def command_add_movie(movies: list):
    """
    Add a new movie to the database after fetching details from the API.

    Args:
        movies (list): Current list of movies in the database.

    Returns:
        None
    """
    while True:
        user_input_title = get_user_input()
        movie_info = api.get_movie(user_input_title)

        if not movie_info:
            print(Fore.RED + f"Movie '{user_input_title}' not found")
            continue

        title, year, rating, image = movie_info

        if is_movie_in_db(title, storage.list_movies()):
            print(Fore.RED + "Your movie already exists")
            continue
        break

    is_added = storage.add_movie(title, year, rating, image)
    if is_added:
        print(Fore.WHITE + f"The movie {title} has been added")
        print(Fore.WHITE + f"{'-' * 40}")


def command_update_movie(movies: list):
    """
       Update the rating of an existing movie in the database.

       Args:
           movies (list): Current list of movies in the database.

       Returns:
           None
    """

    user_input_title = get_user_input()

    if not is_movie_in_db(user_input_title, movies):
        print(Fore.RED + f"Movie '{user_input_title}' not found")
        return

    while True:
        try:
            new_rating = float(input(Fore.GREEN + "Enter the new rating (0-10): "))
            if 0 <= new_rating <= 10:
                break
            else:
                print(Fore.RED + "Rating must be between 0 and 10")

        except ValueError:
            print(Fore.RED + "Rating must be a number")

    is_updated = storage.update_movie(user_input_title, new_rating)

    if is_updated:
        print(Fore.WHITE + f"The movie '{user_input_title}' has been updated")
    else:
        print(Fore.RED + f"Movie '{user_input_title}' not found in database")

    print(Fore.WHITE + f"{'-' * 40}")


def command_delete_movie(movies: list):
    """
    Delete a movie from the database.

    Args:
        movies (list): Current list of movies in the database.

    Returns:
        None
    """
    user_input_title = get_user_input()

    if not is_movie_in_db(user_input_title, movies):
        print(Fore.RED + f"Movie '{user_input_title}' not found")
        return

    is_deleted = storage.delete_movie(user_input_title)

    if is_deleted:
        print(Fore.WHITE + f"The movie {user_input_title} has been deleted")
        print(Fore.WHITE + f"{'-' * 40}")
    else:
        print(Fore.RED + f"I could not find {user_input_title}")
        print(Fore.WHITE + f"{'-' * 40}")


def command_statistics_of_movies(movies: list):
    """
    Print statistics of movies including best, worst, average, and median ratings.

    Args:
        movies (list): List of movies in the database.

    Returns:
        None
    """

    list_of_ratings = []

    if not movies:
        print(Fore.RED + "Database is empty.")
        return

    for movie in movies:
        list_of_ratings.append(movie[2])

    average_rating = sum(list_of_ratings) / len(list_of_ratings)
    max_rating = max(list_of_ratings)
    min_rating = min(list_of_ratings)
    median = statistics.median(list_of_ratings)

    movie_with_max_rating = []
    movie_with_min_rating = []

    for movie in movies:
        if movie[2] == max_rating:
            movie_with_max_rating.append(movie[0])
        if movie[2] == min_rating:
            movie_with_min_rating.append(movie[0])

    print(Fore.WHITE + f"The best movie/movies with rating {max_rating}: ")
    for movie in movie_with_max_rating:
        print(Fore.WHITE + movie)
    print()
    print(Fore.WHITE + f"{'-' * 40}")

    print(Fore.WHITE + f"The worst movie/movies with rating {min_rating}: ")
    for movie in movie_with_min_rating:
        print(Fore.WHITE + movie)
    print()
    print(Fore.WHITE + f"{'-' * 40}")

    print(Fore.WHITE + f"The average rating: {average_rating:.1f}\n"
                       f"The median rating: {median}\n")
    print(Fore.WHITE + f"{'-' * 40}")


def command_select_random_movie(movies: list):
    """
    Select and print a random movie from the database.

    Args:
        movies (list): List of movies in the database.

    Returns:
        None
    """

    if not movies:
        print(Fore.RED + "Database is empty.")
        return

    random_movie = random.choice(movies)
    title = random_movie[0]
    rating = random_movie[2]

    print(Fore.WHITE + f"Your movie for today is ´{title}´: {rating}")
    print(Fore.WHITE + f"{'-' * 40}")


def command_searching_movie(movies: list):
    """
    Search movies by a substring of the title and print results.

    Args:
        movies (list): List of movies in the database.

    Returns:
        None
    """

    if not movies:
        print(Fore.RED + "Database is empty.")
        return

    user_input_title = get_user_input()
    list_of_all_movies_we_found = []

    for movie in movies:
        if user_input_title.lower() in movie[0].lower():
            list_of_all_movies_we_found.append(movie)

    if not list_of_all_movies_we_found:
        print(Fore.RED + f"I could not find ´{user_input_title}´")
        print(Fore.WHITE + f"{'-' * 40}")

    else:
        print("Movie/movies, we found: ")
        for movie in list_of_all_movies_we_found:
            print(Fore.WHITE + f'{movie[0]}, {movie[2]}, {movie[1]}')
        print(Fore.WHITE + f"{'-' * 40}")


def command_sorted_by_rating(movies: list):
    """
    Print the list of movies sorted by rating in descending order.

    Args:
        movies (list): List of movies in the database.

    Returns:
        None
    """

    if not movies:
        print(Fore.RED + "Database is empty.")
        return

    sorted_movies = sorted(movies, key=lambda movie: movie[2], reverse=True)
    print(Fore.WHITE + "Sorted list of  movies:")
    for movie in sorted_movies:
        print(Fore.WHITE + f'{movie[0]}, {movie[2]}, {movie[1]}')
    print(Fore.WHITE + f"{'-' * 40}")


def command_histogram(movies: list):
    """
    Display a histogram of movies by rating and save as PNG or JPEG.

    Args:
        movies (list): List of movies in the database.

    Returns:
        None
    """

    saving_in = input(Fore.GREEN + "In what format do you want to save the histogram (png, jpeg)?: ").lower()

    ratings = []

    if not movies:
        print(Fore.RED + "Database is empty.")
        return

    for movie in movies:
        ratings.append(movie[2])

    plt.hist(ratings, width=0.5, bins=10, linewidth=0.5)
    plt.title("Histogram of movies")
    plt.xlabel("ratings")
    plt.ylabel("movies number")

    if saving_in == "png":
        plt.savefig('mein_histogram.png')
        plt.show()
    elif saving_in == "jpeg":
        plt.savefig('mein_histogram.jpeg')
        plt.show()


def command_generate_website(movies: list):
    """
    Generate a static HTML page showing all movies.

    Args:
        movies (list): List of movies in the database.

    Returns:
        None
    """

    html_page_template = web.load_html("static/index_template.html")
    new_html_string = ""

    if movies:
        for movie in movies:
            new_html_string = new_html_string + web.serialize_movie(movie[0], movie[1], movie[3])

        html_page_movies = html_page_template.replace("__TEMPLATE_MOVIE_GRID__", new_html_string)
        web.save_html("static/index.html", html_page_movies)
        print(Fore.WHITE + "Website was generated successfully")
        return
    else:
        html_page_movies = html_page_template.replace("__TEMPLATE_MOVIE_GRID__",
                                                      "<h2>There are no movies here yet</h2>")
        web.save_html("static/index.html", html_page_movies)
        print(Fore.WHITE + "Website was generated successfully")
        return


def user_select_command(movies: list, function_dictionary: dict):
    """
    Run the command selected by the user from the main menu.

    Args:
        movies (list): Current list of movies in the database.
        function_dictionary (dict): Dictionary mapping menu options to functions.

    Returns:
        None
    """

    while True:
        select_option = print_menu_and_select_from_the_main_menu()

        if select_option == "0":
            print(Fore.WHITE + "Bye!")
            break

        if select_option in function_dictionary:
            function_dictionary[select_option](storage.list_movies())
            input(Fore.GREEN + "Press Enter to back to menu ")
        else:
            print(Fore.RED + "The number is out of menu")
            continue


def main():
    movies = storage.list_movies()

    func_dict = {"1": command_list_movies,
                 "2": command_add_movie,
                 "3": command_update_movie,
                 "4": command_delete_movie,
                 "5": command_statistics_of_movies,
                 "6": command_select_random_movie,
                 "7": command_searching_movie,
                 "8": command_sorted_by_rating,
                 "9": command_histogram,
                 "10": command_generate_website}

    print(Fore.YELLOW + f"{'*' * 20} My Movies Database {'*' * 20}")
    user_select_command(movies, func_dict)


if __name__ == "__main__":
    main()
