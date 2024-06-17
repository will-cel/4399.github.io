# app.py

from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Initialize the Flask application
app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Define the database model
class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    rating = db.Column(db.Float)

    def __init__(self, name, rating):
        self.name = name
        self.rating = rating

    def __repr__(self):
        return f"<Movie {self.name} - {self.rating}>"

# Create the database
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def index():
    movies = Movie.query.all()
    return render_template('index.html', movies=movies)

# Add movie route
@app.route('/add', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        name = request.form['name']
        rating = request.form['rating']
        new_movie = Movie(name=name, rating=rating)
        db.session.add(new_movie)
        db.session.commit()
        flash('Movie added successfully!')
        return redirect(url_for('index'))
    return render_template('add.html')

# Edit movie route
@app.route('/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':
        movie.name = request.form['name']
        movie.rating = request.form['rating']
        db.session.commit()
        flash('Movie updated successfully!')
        return redirect(url_for('index'))
    return render_template('edit.html', movie=movie)

# Delete movie route
@app.route('/delete/<int:movie_id>')
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    flash('Movie deleted successfully!')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
