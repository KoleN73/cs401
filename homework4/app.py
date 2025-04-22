import json
import logging

from flask import Flask, request

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

# Helper function to retrieve data from the movies.json file
def get_data() -> list[dict]:
    """
    Retrieve the movies dataset and return it as a list of dictionaries.

    Returns:
        data (list[dict]): A list of dictionaries containing the movies dataset.
    """
    with open('movies.json', 'r') as file:
    
        data = json.load(file)

    return data


# DONE: Add a route to return the entire dataset
@app.route('/movies', methods=['GET'])
def get_all_movies():
    """
    Return the entire movies dataset.

    Returns:
        response (json): A JSON response containing all movies.
    """
    logging.debug("Fetching entire movie dataset")
    try:
        data = get_data()
        return data, 200
    except Exception as e:
        logging.error(f"Error retrieving movie data: {e}")
        return {"error": "Unable to fetch data"}, 500

# DONE: Add a route to return the movies that are between 2020-2022
@app.route('/movies/2020s', methods=['GET'])
def get_movies_from_2020_to_2022():
    """
    Return movies released between 2020 and 2022 (inclusive).

    Returns:
        JSON list of movies from 2020 to 2022.
    """
    logging.debug("Fetching movies released between 2020 and 2022")
    try:
        data = get_data()
        filtered = [movie for movie in data if 2020 <= movie.get("Year", 0) <= 2022]
        return filtered, 200
    except Exception as e:
        logging.error(f"Error fetching 2020s movies: {e}")
        return {"error": "Unable to retrieve 2020s movies"}, 500


# Done: Add a route to return a movie if it matches the id queried
@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie_by_id(movie_id):
    """
    Return a single movie by its ID.

    Args:
        movie_id (int): Movie ID

    Returns:
        JSON object of the movie
    """
    logging.debug(f"Looking for movie with ID: {movie_id}")
    try:
        data = get_data()
        movie = next((m for m in data if m.get('id') == movie_id), None)
        if movie:
            return movie, 200
        return {"error": "Movie not found"}, 404
    except Exception as e:
        logging.error(f"Error fetching movie by ID: {e}")
        return {"error": "Unable to fetch movie"}, 500


# DONE: Add a route to return the genres for a specific movie
@app.route('/movies/genre/action', methods=['GET'])
def get_action_movies():
    """
    Return all movies that include 'Action' in their genre list.

    Returns:
        JSON list of action movies.
    """
    logging.debug("Fetching movies with genre 'Action'")
    try:
        data = get_data()
        filtered = [movie for movie in data if "Action" in movie.get("genres", [])]
        return filtered, 200
    except Exception as e:
        logging.error(f"Error filtering by genre 'Action': {e}")
        return {"error": "Unable to retrieve action movies"}, 500
    

# DONE: Add a route to return movies that won 2 or more oscars
@app.route('/movies/prettyalright', methods=['GET'])
def get_movies_with_2_or_more_oscars():
    """
    Return all movies that have 2 or more oscars.

    Returns:
        JSON list of movies with oscars >= 2.
    """
    logging.debug("Fetching movies with 2 or more oscars")
    try:
        data = get_data()
        filtered = [movie for movie in data if movie.get("oscars", 0) >= 2]
        return filtered, 200
    except Exception as e:
        logging.error(f"Error filtering movies with 2+ oscars: {e}")
        return {"error": "Unable to retrieve movies with 2+ oscars"}, 500
    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')