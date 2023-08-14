# movieflix_db

A Full Stack Python project managing users and movies data from sqlite relational database using Flask SQLAlchemy ORM and Jinja2.

### Entities:
- User
- Movie
- UserMovie
- MovieReview

Using blueprints for users and movies routes.

Entities input form validations and error handling with app’s routes error handlers.

Improve user experience using Google Fonts and Bootstrap.

Fetching movie info from external API imdb website, using requests.

Implementing OOP concepts: Interface and polymorphism for data management layer.

Automated testing with pytest.


### Offering Movieflix app as a web service with API endpoints:

Users:
- GET /api/users: List all users.
- POST /api/users: Add a new user.
- GET /api/users/<user_id>/movies: List a user’s favorite movies.
- POST /api/users/<user_id>/movies/<movie_id>: Add a new favorite movie for a user.
- DELETE /api/users/movies/<user_movie_id>: Delete a favorite movie for a user.

Movies:
- GET /api/movies: List all movies.
- POST /api/movies: Add a new movie.
- PATCH /api/movies/update_movie/<int:movie_id>: Update a movie.
- DELETE /api/movies/delete_movie/<int:movie_id>: Delete a movie.
- GET /api/movies/<int:movie_id>/reviews: List all movie reviews for a movie
- POST /api/users/<int:user_id>/add_movie_review/<int:movie_id>: Add a movie review for a movie


![all_movies.png](static%2Fimages%2Fall_movies.png)

![fav_movie.png](static%2Fimages%2Ffav_movie.png)

![movie_review.png](static%2Fimages%2Fmovie_review.png)

![error_update.png](static%2Fimages%2Ferror_update.png)
