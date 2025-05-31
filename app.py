from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
import uuid

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a strong secret key for sessions

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///song.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Assign user_id to every new session
@app.before_request
def assign_user():
    if 'user_id' not in session:
        session['user_id'] = str(uuid.uuid4())

class Song(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    movie = db.Column(db.String(100), nullable=False)
    artist = db.Column(db.String(100), nullable=False)
    write = db.Column(db.String(100), nullable=False)
    music = db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    label = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.String(100), nullable=False)  # 👈 Add user_id

    def __repr__(self):
        return f"{self.sno} - {self.name}"

@app.route("/", methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        name = request.form['name']
        movie = request.form['movie']
        artist = request.form['artist']
        write = request.form['write']
        music = request.form['music']
        genre = request.form['genre']
        label = request.form['label']
        user_id = session['user_id']  # Get current user's ID

        song = Song(
            name=name,
            movie=movie,
            artist=artist,
            write=write,
            music=music,
            genre=genre,
            label=label,
            user_id=user_id
        )
        db.session.add(song)
        db.session.commit()

    # Show only current user's songs
    allsong = Song.query.filter_by(user_id=session['user_id']).all()
    return render_template('index.html', allsong=allsong)

@app.route('/search')
def search():
    query = request.args.get('search', '').lower()
    user_id = session['user_id']
    results = Song.query.filter_by(user_id=user_id).filter(
        Song.name.ilike(f'%{query}%') |
        Song.movie.ilike(f'%{query}%') |
        Song.artist.ilike(f'%{query}%') |
        Song.write.ilike(f'%{query}%') |
        Song.music.ilike(f'%{query}%') |
        Song.genre.ilike(f'%{query}%') |
        Song.label.ilike(f'%{query}%')
    ).all()
    return render_template('search.html', songs=results, query=query)

@app.route("/about")
def About():
    return render_template('about.html')

@app.route("/techused")
def Tech():
    return render_template('tech.html')

@app.route("/myviews")
def myview():
    return render_template('myview.html')

@app.route("/update/<int:sno>", methods=['GET', 'POST'])
def update(sno):
    song = Song.query.filter_by(sno=sno, user_id=session['user_id']).first()
    if not song:
        return redirect("/")

    if request.method == "POST":
        song.name = request.form['name']
        song.movie = request.form['movie']
        song.artist = request.form['artist']
        song.write = request.form['write']
        song.music = request.form['music']
        song.genre = request.form['genre']
        song.label = request.form['label']
        db.session.commit()
        return redirect("/")

    return render_template('update.html', song=song)

@app.route("/delete/<int:sno>")
def delete(sno):
    song = Song.query.filter_by(sno=sno, user_id=session['user_id']).first()
    if song:
        db.session.delete(song)
        db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)
