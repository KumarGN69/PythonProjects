from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests
from pprint import pprint

# '''
# Red underlines? Install the required packages first: 
# Open the Terminal in PyCharm (bottom left). 

# On Windows type:
# python -m pip install -r requirements.txt

# On MacOS type:
# pip3 install -r requirements.txt

# # This will install the packages from requirements.txt for this project.
# # '''
all_movies = []
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

# CREATE DB
class Base(DeclarativeBase):
    pass


app.config['SQLALCHEMY_DATABASE_URI'] ="sqlite:///my-top-100movies.db"
db = SQLAlchemy(model_class=Base)
db.init_app(app)

# CREATE TABLE
class Movie(db.Model):
    id: Mapped[int] = mapped_column(Integer, nullable=False, primary_key=True)
    title: Mapped[str] = mapped_column(String(250), unique= True, nullable=False)
    year: Mapped[str] = mapped_column(String(4),nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    rating: Mapped[float] = mapped_column(Float, nullable=False)
    ranking: Mapped[int] = mapped_column(Integer, nullable=False)
    review: Mapped[str] = mapped_column(String(150), nullable=False)
    img_url: Mapped[str] = mapped_column(String(1000), nullable=False)

    def __repr__(self) -> str:
        return f"{self.title}"

class ReviewForm(FlaskForm):
    rating = StringField (label="Your rating of 10 eg:7.5", validators=[DataRequired()])
    review = StringField(label="Review", validators=[DataRequired()])
    submit = SubmitField(label="Done")


with app.app_context():
    db.session.close()
    db.drop_all()
    db.create_all()
    movie1 = Movie(    
            title="Avatar The Way of Water",
            year=2022,
            description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
            rating=8.3,
            ranking=10,
            review="I liked the water.",
            img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg")
    db.session.add(movie1)
    movie2 = Movie(    
            title="Phone Booth",
            year=2002,
            description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
            rating=7.3,
            ranking=10,
            review="My favourite character was the caller.",
            img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg")
    db.session.add(movie2)
    db.session.commit()


@app.route("/")
def home():
    global all_movies
    with app.app_context():
        result = db.session.execute(db.select(Movie).order_by(Movie.title))
        # all_movies = Movie.query.scalars().fetchall()
        all_movies = result.scalars().fetchall()
        print(all_movies)
    return render_template("index.html", movies=all_movies)

@app.route("/edit", methods=["GET","POST"])
def edit():
    form = ReviewForm()
    movie_id = request.args.get('id')
    movie = db.get_or_404(Movie,movie_id)

    return render_template("edit.html", movie=movie, form=form)

if __name__ == '__main__':
    app.run(debug=True)
