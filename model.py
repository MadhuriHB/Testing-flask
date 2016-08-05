from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Game(db.Model):
    """Board game."""

    __tablename__ = "games"
    game_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    description = db.Column(db.String(100))


def connect_to_db(app, db_uri="postgresql:///testdb"):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)


def example_data():
    """Create example data for the test database."""
    #FIXME: write a function that creates a game and adds it to the database.
    game1 = Game(name="Chess", description="War simulations")
    game2 = Game(name="Bingo", description="The game grandparents play at church on Sunday night")

    db.session.add(game1)
    db.session.add(game2)
    db.session.commit()
    
    # :print "FIXME"


if __name__ == '__main__':
    
    from server import app

    connect_to_db(app)
    print "Connected to DB."
    