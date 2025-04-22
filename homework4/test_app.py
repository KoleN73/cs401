import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

# 1. Test entire dataset route
def test_get_all_movies(client):
    response = client.get('/movies')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)
    assert len(data) >= 5

    for i, movie in enumerate(data[:5]):
        assert "Title" in movie
        assert "Year" in movie
        assert isinstance(movie.get("Title"), str)
        assert isinstance(movie.get("Year"), int)
        assert isinstance(movie, dict)

# 2. Test year range route (2020s)
def test_get_movies_2020s(client):
    response = client.get('/movies/2020s')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

    for i, movie in enumerate(data[:5]):
        assert 2020 <= movie.get("Year", 0) <= 2022
        assert "MPA" in movie
        assert isinstance(movie["MPA"], str)
        assert "Duration" in movie
        assert isinstance(movie["Duration"], int)

# 3. Test movie by ID (1 to 5)
def test_get_movie_by_id(client):
    for movie_id in [1, 2, 3, 4, 5]:
        response = client.get(f'/movies/{movie_id}')
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            movie = response.get_json()
            assert "Rating" in movie
            assert isinstance(movie["Rating"], (int, float))
            assert "Title" in movie
            assert isinstance(movie["Title"], str)
            assert isinstance(movie.get("id"), int)

# 4. Test genre route (Action)
def test_get_action_movies(client):
    response = client.get('/movies/genre/action')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

    for i, movie in enumerate(data[:5]):
        genres = movie.get("genres", [])
        assert isinstance(genres, list)
        assert "Action" in genres
        assert "Votes" in movie
        assert isinstance(movie["Votes"], int)
        assert "Title" in movie

# 5. Test movies with 2+ oscars
def test_get_movies_with_oscars(client):
    response = client.get('/movies/prettyalright')
    assert response.status_code == 200
    data = response.get_json()
    assert isinstance(data, list)

    for i, movie in enumerate(data[:5]):
        assert movie.get("oscars", 0) >= 2
        assert "directors" in movie
        assert isinstance(movie["directors"], list)
        assert "Title" in movie
        assert isinstance(movie["Title"], str)

# 6. Test invalid URL
def test_invalid_route(client):
    response = client.get('/movies/notarealroute')
    assert response.status_code == 404