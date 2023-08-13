from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_name = db.Column(db.String)
    movies = db.relationship('UserMovie', back_populates='user', cascade='all, delete-orphan')
    movie_reviews = db.relationship('MovieReview', back_populates='user', cascade='all, delete-orphan')  # New relationship

    def __repr__(self) -> str:
        return f"User(id={self.id}, user_name={self.user_name})"

    def __str__(self) -> str:
        return f"User info:\n" \
               f"id: {self.id}\n" \
               f"user_name: {self.user_name}"


class Movie(db.Model):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    movie_name = db.Column(db.String(50), unique=True)
    director = db.Column(db.String(50))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float, default=0.0)
    poster = db.Column(db.String)
    website = db.Column(db.String)
    users = db.relationship('UserMovie', back_populates='movie')
    movie_reviews = db.relationship('MovieReview', back_populates='movie')  # New relationship

    def __repr__(self) -> str:
        return f"Movie(id={self.id}, " \
               f"movie_name={self.movie_name}, " \
               f"year={self.year}, " \
               f"rating={self.rating})"

    def __str__(self) -> str:
        return f"Movie info:\n" \
               f"id: {self.id}\n" \
               f"movie_name: {self.movie_name}\n" \
               f"year: {self.year}\n" \
               f"rating: {self.rating}"


class UserMovie(db.Model):
    __tablename__ = "users_movies"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'), nullable=False)

    user = db.relationship('User', back_populates='movies')
    movie = db.relationship('Movie', back_populates='users')


class MovieReview(db.Model):
    """
    MovieReview Class
    """
    __tablename__ = "movies_reviews"
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.id'))
    review_text = db.Column(db.String)
    rating = db.Column(db.Float, default=0.0)

    user = db.relationship('User', back_populates='movie_reviews')
    movie = db.relationship('Movie', back_populates='movie_reviews')
