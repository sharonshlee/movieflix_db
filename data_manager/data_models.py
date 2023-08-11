from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """
    User class
    """
    __tablename__ = 'users'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    user_name = db.Column(db.String)
    movies = db.relationship('Movie', back_populates='user', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f"User(user_id={self.id}, " \
               f"user_name={self.user_name})"

    def __str__(self) -> str:
        return f"""User info:
                    user_id: {self.id},
                    user_name: {self.user_name}
                """


class Movie(db.Model):
    """
    Movie Class
    """
    __tablename__ = 'movies'
    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    movie_name = db.Column(db.String(50), unique=True)
    director = db.Column(db.String(50))
    year = db.Column(db.Integer)
    rating = db.Column(db.Float, default=0.0)
    poster = db.Column(db.String)
    website = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Create a relationship between Movie and User
    user = db.relationship('User', back_populates='movies')

    def __repr__(self) -> str:
        return f"Movie(movie_id={self.id}, " \
               f"movie_name={self.movie_name}, " \
               f"year={self.year}, " \
               f"rating={self.rating}, " \
               f"poster={self.poster}, " \
               f"website={self.website}, " \
               f"user_id={self.user_id})"

    def __str__(self) -> str:
        return f"""Movie info:
                    movie_id: {self.id},
                    movie_name: {self.movie_name},
                    year: {self.year},
                    rating: {self.rating},
                    poster: {self.poster},
                    website: {self.website},
                    user_id={self.user_id}
                """
