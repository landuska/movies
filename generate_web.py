def load_html(file_path):
    """
    Reads the content of an HTML file from the specified path.

    Args:
        file_path (str): The path to the HTML file to be loaded.

    Returns:
        str: The content of the file as a string.
             Returns an empty string if the file is not found or an error occurs.
    """

    try:
        with open(file_path, "r") as file:
            return file.read()

    except FileNotFoundError:
        print("HTML file not found")
        return ""

    except PermissionError:
        print("Permission error")
        return ""

    except OSError as e:
        print(f"File error: {e}")
        return ""


def save_html(file_path, content):
    """
    Writes the provided HTML content to a file at the given path.

    Args:
        file_path (str): The destination path where the file should be saved.
        content (str): The HTML string to be written into the file.

    Returns:
        None
    """

    try:
        with open(file_path, "w") as file:
            file.write(content)

    except PermissionError:
        print("Cannot write file (permission denied)")

    except OSError as e:
        print(f"File error: {e}")


def serialize_movie(title, year, image):
    """
    Generate an HTML list item representing a movie with its poster, title, and year.

    Args:
        title (str): The title of the movie.
        year (str or int): The release year of the movie.
        image (str): The URL or path to the movie's poster image.

    Returns:
        str: An HTML string representing the movie as a list item.
    """

    output_string = ''
    output_string += '<li>'
    output_string += '<div class="movie">\n'
    output_string += f'<img class="movie-poster" src="{image}">\n'
    output_string += f'<div class="movie-title">{title}</div>\n'
    output_string += f'<div class="movie-year">{year}</div>\n'
    output_string += '</div>\n'
    output_string += '</li>\n'
    return output_string
