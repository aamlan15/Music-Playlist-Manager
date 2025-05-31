from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
import sqlite3
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///song.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db=SQLAlchemy(app)

class Song(db.Model):
    sno=db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    movie=db.Column(db.String(100), nullable=False)
    artist=db.Column(db.String(100), nullable=False)
    write=db.Column(db.String(100), nullable=False)
    music=db.Column(db.String(100), nullable=False)
    genre = db.Column(db.String(100), nullable=False)
    label=db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"{self.sno} - {self.name}"

@app.route("/",methods=['GET','POST'])
def home():
    if request.method=="POST":
        name=request.form['name']
        movie=request.form['movie']
        artist=request.form['artist']
        write=request.form['write']
        music=request.form['music']
        genre=request.form['genre']
        label=request.form['label']
        song=Song(name=name,movie=movie,artist=artist,write=write,music=music,genre=genre,label=label)
        db.session.add(song)
        db.session.commit()
    allsong=Song.query.all()
    return render_template('index.html',allsong=allsong)


@app.route('/search')
def search():
    query = request.args.get('search', '').lower()

    # Case-insensitive search using SQLAlchemy's ilike (for SQLite)
    results = Song.query.filter(
        Song.name.ilike(f'%{query}%') |
        Song.movie.ilike(f'%{query}%') |
        Song.artist.ilike(f'%{query}%') |
        Song.write.ilike(f'%{query}%') |
        Song.music.ilike(f'%{query}%') |
        Song.genre.ilike(f'%{query}%') |
        Song.label.ilike(f'%{query}%')
    ).all()

    return render_template('search.html', songs=results, query=query)

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

@app.route("/update/<int:sno>",methods=['GET','POST'])
def update(sno):
    if request.method=="POST":
        name=request.form['name']
        movie=request.form['movie']
        artist=request.form['artist']
        write=request.form['write']
        music=request.form['music']
        genre=request.form['genre']
        label=request.form['label']
        song=Song.query.filter_by(sno=sno).first()
        song.name=name
        song.movie=movie
        song.artist=artist
        song.write=write
        song.music=music
        song.genre=genre
        song.label=label
        db.session.add(song)
        db.session.commit()
        return redirect("/")

    song=Song.query.filter_by(sno=sno).first()
    return render_template('update.html',song=song)

@app.route("/delete/<int:sno>")
def delete(sno):
    song=Song.query.filter_by(sno=sno).first()
    db.session.delete(song)
    db.session.commit()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True)
