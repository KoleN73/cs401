from analyze_data import net_profit, average_budget_last_5_years, most_common_title_word
import pytest

def test_net_profit():
    # Test case 1: Basic example
    movies = [
        {"Title": "Movie A", "Year": 2023, "budget": 100, "grossWorldWide": 500},
        {"Title": "Movie B", "Year": 2022, "budget": 200, "grossWorldWide": 700}
    ]
    result = net_profit(movies)
    assert result["Title"] == "Movie B"

    # Test case 2: No recent movies
    movies = [
        {"Title": "Old Movie", "Year": 2010, "budget": 100, "grossWorldWide": 500}
    ]
    assert net_profit(movies) is None

    # Test case 3: Missing financial data
    movies = [
        {"Title": "Incomplete", "Year": 2023},
        {"Title": "Valid", "Year": 2023, "budget": 100, "grossWorldWide": 600}
    ]
    assert net_profit(movies)["Title"] == "Valid"

def test_average_budget_last_5_years():
    # Test case 1: Basic average
    movies = [
        {"Title": "A", "Year": 2021, "budget": 100},
        {"Title": "B", "Year": 2022, "budget": 300}
    ]
    avg = average_budget_last_5_years(movies)
    assert avg == 200.0

    # Test case 2: No valid budgets
    movies = [
        {"Title": "A", "Year": 2021},
        {"Title": "B", "Year": 2022, "budget": "unknown"}
    ]
    assert average_budget_last_5_years(movies) is None

    # Test case 3: Some valid, some invalid
    movies = [
        {"Title": "A", "Year": 2023, "budget": 200},
        {"Title": "B", "Year": 2023},
        {"Title": "C", "Year": 2023, "budget": 400}
    ]
    assert average_budget_last_5_years(movies) == 300.0

def test_most_common_title_word():
    # Test case 1: Common word
    movies = [
        {"Title": "The Big Game"},
        {"Title": "Game Night"},
        {"Title": "Game On"}
    ]
    assert most_common_title_word(movies) == "game"

    # Test case 2: Mixed casing and punctuation
    movies = [
        {"Title": "Love, Actually"},
        {"Title": "Truly Love"},
        {"Title": "What is Love?"}
    ]
    assert most_common_title_word(movies) == "love"

    # Test case 3: Empty title strings
    movies = [
        {"Title": ""},
        {"Title": " ", "Year": 2022}
    ]
    assert most_common_title_word(movies) is None