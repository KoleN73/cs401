import sys
import json
import logging
from datetime import datetime                     #Needed for 5 year function
from typing import List, Dict, Optional, Union    #Needed for type hints

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(levelname)s:%(message)s')

def read_json(filepath: str) -> Optional[List[Dict]]: 
    """
    Description:
        Reads a JSON file and loads the content into a list of dictionaries.

    Args:
        filepath (str): Path to the JSON file.

    Returns:
        list[dict] | None: Parsed JSON data as a list of movie dictionaries, or None on error.
    """
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            logging.debug(f"Successfully loaded {len(data)} records from {filepath}.")
            return data
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.debug(f"Failed to load JSON file: {e}")
        return None

def net_profit(movies: List[Dict]) -> Optional[Dict]:
    """
    Description:
        Finds the movie with the largest net profit from the last 5 years.

    Args:
        movies (list): List of movie dictionaries.

    Returns:
        dict | None: Movie with the highest net profit, or None if no valid movie is found.
    """
    current_year = datetime.now().year
    recent_movies = [m for m in movies if m.get("Year") and (current_year - m["Year"] <= 5)]

    max_profit = float('-inf')
    best_movie = None

    for movie in recent_movies:
        budget = movie.get("budget")
        gross = movie.get("grossWorldWide")

        if isinstance(budget, (int, float)) and isinstance(gross, (int, float)):
            profit = gross - budget
            if profit > max_profit:
                max_profit = profit
                best_movie = movie

    logging.debug(f"Most profitable movie: {best_movie.get('Title') if best_movie else 'None'}")
    return best_movie

def print_movie_summary(movie: Optional[Dict]) -> None:
    """
    Description:
        Prints a summary of the movie details.

    Args:
        movie (dict): Movie dictionary.

    Returns:
        None
    """
    if movie:
        print(f"Title: {movie.get('Title')}")
        print(f"Year: {movie.get('Year')}")
        print(f"Net Profit: ${movie.get('grossWorldWide') - movie.get('budget'):,.2f}")
        print(f"Budget: ${movie.get('budget'):,.2f}")
        print(f"Gross Worldwide: ${movie.get('grossWorldWide'):,.2f}")
    else:
        print("No valid movie found within the past 5 years.")

def average_budget_last_5_years(movies: List[Dict]) -> Optional[float]:
    """
    Description:
        Calculates the average budget of movies released in the past 5 years.

    Args:
        movies (list): List of movie dictionaries.

    Returns:
        float | None: Average budget value or None if no data is available.
    """
    current_year = datetime.now().year
    recent_budgets = [
        m["budget"] for m in movies
        if m.get("Year") and (current_year - m["Year"] <= 5) and isinstance(m.get("budget"), (int, float))
    ]

    if not recent_budgets:
        logging.debug("No recent movie budgets found.")
        return None

    avg_budget = sum(recent_budgets) / len(recent_budgets)
    logging.debug(f"Average budget: {avg_budget}")
    print(f"Average Budget (Last 5 Years): ${avg_budget:,.2f}")
    return avg_budget

def most_common_title_word(movies: List[Dict]) -> Optional[str]:
    """
    Description:
        Finds the most frequent word used in movie titles.

    Args:
        movies (list): List of movie dictionaries.

    Returns:
        str | None: Most common word in movie titles.
    """
    word_count = {}
    for movie in movies:
        title = movie.get("Title", "")
        words = title.split()
        for word in words:
            cleaned = word.strip(".,:!?()[]").lower()
            word_count[cleaned] = word_count.get(cleaned, 0) + 1

    if not word_count:
        logging.debug("No title words to analyze.")
        return None

    most_common = max(word_count.items(), key=lambda item: item[1])
    logging.debug(f"Most common word: {most_common[0]}")
    print(f"Most Common Word in Titles: '{most_common[0]}' ({most_common[1]} times)")
    return most_common[0]

def main():
    if len(sys.argv) < 2:
        print("Error: No command line argument provided. Please provide a file name for a JSON file to read.")
        sys.exit(1)

    filepath = sys.argv[1]
    data = read_json(filepath)

    if not data:
        print("Failed to read or parse JSON file.")
        return

    print(f"\nLoaded {len(data)} movies from {filepath}\n")
    top_movie = net_profit(data)
    print_movie_summary(top_movie)
    average_budget_last_5_years(data)
    most_common_title_word(data)

if __name__ == '__main__':
    main()
