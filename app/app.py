from flask import Flask,render_template, session, request, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import pymysql
# pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KaVGm31asLwNAlaoG'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/emoji'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Rombel(db.Model):
    __tablename__ = 'rombel'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50), nullable=False)

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50))
    rombel_id = db.Column(db.Integer, db.ForeignKey('rombel.id'), nullable=False)
    gambar = db.Column(db.String(50))


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/materi')
def materi():
    return render_template('materi/materi.html')

@app.route('/materi/emosi-dasar')
def materi_emosi_dasar():
    return render_template('materi/materi-emosi-dasar.html')

@app.route('/materi/emosi-gabungan')
def materi_emosi_gabungan():
    return render_template('materi/materi-emosi-gabungan.html')

@app.route('/latihan')
def latihan():
    return render_template('latihan/latihan.html')

@app.route('/latihan/rombel/emosi-dasar')
def latihan_rombel_dasar():
    rombel = Rombel.query.all()
    return render_template('latihan/latihan-emosi-dasar.html', rombel=rombel)

@app.route('/latihan/rombel/emosi-gabungan')
def latihan_rombel_gabungan():
    rombel = Rombel.query.all()
    return render_template('latihan/latihan-emosi-gabungan.html', rombel=rombel)

@app.route('/latihan/emosi-dasar/rombel/<rombongan>')
def latihan_rombel(rombongan):
    users = User.query.filter_by(rombel_id=rombongan).all()
    return render_template('latihan/latihan-rombel.html', users=users)

@app.route('/latihan/rombel/emosi/siswa/pilih-emosi')
def latiha_pilih_emosi():
    return render_template('latihan/latihan-pemilihan-emosi.html')

if __name__ == '__main__':
    app.run(debug=True)