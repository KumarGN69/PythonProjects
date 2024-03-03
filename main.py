from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
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
    ranking = StringField(label="Ranking", validators=[DataRequired()])
    submit = SubmitField(label="Done")

class AddForm(FlaskForm):
    title = StringField (label="Name of the movie", validators=[DataRequired()])
    year = StringField(label="Year the movie was made", validators=[DataRequired()])
    description= StringField(label="Storyline of the movie", validators=[DataRequired()])
    rating = StringField(label= "Enter you rating for the movie eg: 7.6 of 10", validators=[DataRequired()])
    ranking = StringField(label= "How would you rank the movie from 1-10?", validators=[DataRequired()])
    review = StringField(label= "SHort review for movie", validators=[DataRequired()])
    img_url = StringField(label= "Enter the link to the poster for the movie", validators=[DataRequired()])
    submit = SubmitField(label="Add")
with app.app_context():
    # db.session.close()
    # db.drop_all()
    db.create_all()
    # movie1 = Movie(    
    #         title="Avatar The Way of Water",
    #         year=2022,
    #         description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
    #         rating=8.3,
    #         ranking=10,
    #         review="I liked the water.",
    #         img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg")
    # db.session.add(movie1)
    # movie2 = Movie(    
    #         title="Phone Booth",
    #         year=2002,
    #         description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads to a jaw-dropping climax.",
    #         rating=7.3,
    #         ranking=10,
    #         review="My favourite character was the caller.",
    #         img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg")
    # db.session.add(movie2)
    # db.session.commit()


@app.route("/")
def home():
    global all_movies
    with app.app_context():
        result = db.session.execute(db.select(Movie).order_by(Movie.ranking))
        # all_movies = Movie.query.scalars().fetchall()
        all_movies = result.scalars().fetchall()
        print(all_movies)
    return render_template("index.html", movies=all_movies)

@app.route("/edit", methods=["GET","POST"])
def edit_movie():
    form = ReviewForm()
    movie_id = request.args.get('id')
    movie = db.get_or_404(Movie,movie_id)
    if form.validate_on_submit():
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        movie.ranking = form.ranking.data
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("edit.html", movie=movie, form=form)

@app.route("/delete", methods=["GET","POST"])
def delete_movie():
    movie_id = request.args.get('id')
    Movie.query.filter_by(id=movie_id).delete()
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/add", methods=["GET","POST"])
def add_movie():
    form = AddForm()
    print("Its here")
    if form.validate_on_submit():
        print("Its inside submit")
        new_movie = Movie(
                    title = form.title.data,
                    year = form.year.data,
                    description = form.description.data,
                    rating = form.rating.data,
                    ranking = form.ranking.data,
                    review = form.review.data,
                    img_url = form.img_url.data
                    )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template("add.html",form=form)
        
if __name__ == '__main__':
    app.run(debug=True)
