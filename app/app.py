from flask import Flask,render_template, session, request, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import pymysql
# pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KaVGm31asLwNAlaoG'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/emojii'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Rombel(db.Model):
    __tablename__ = 'rombel'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f'<Rombel {self.id} {self.nama}>'
    
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(50))
    rombel_id = db.Column(db.Integer, db.ForeignKey('rombel.id'), nullable=False)
    gambar = db.Column(db.String(50))

    def __repr__(self):
        return f'<User {self.id} - {self.rombel_id} - {self.gambar}>'

class JenisEmosi(db.Model):
    __tablename__ = 'jenis_emosi'
    id = db.Column(db.Integer, primary_key=True)
    jenis = db.Column(db.String(50))

    def __repr__(self):
        return f'<JenisEmosi {self.id} - {self.jenis}>'

class Materi(db.Model):
    __tablename__ = 'materi'
    id = db.Column(db.Integer, primary_key=True)
    nama_emosi = db.Column(db.String(50))
    jenis_emosi = db.Column(db.Integer, db.ForeignKey('jenis_emosi.id'), nullable=False)
    gambar_satu = db.Column(db.String(50))
    gambar_dua = db.Column(db.String(50))
    vidio = db.Column(db.String(50))
    emoji = db.Column(db.String(50))

    jenis_emosi_rel = db.relationship('JenisEmosi', backref='materis')

    def __repr__(self):
        return f'{self.jenis_emosi} - {self.nama_emosi}'


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/materi')
def materi():
    return render_template('materi/materi.html')

@app.route('/materi/emosi-dasar')
def materi_emosi_dasar():
    list_nama_emosi =  Materi.query.filter_by(jenis_emosi=1).all()
    return render_template('materi/materi-emosi-dasar.html', 
                               list_nama_emosi=list_nama_emosi
                               )

@app.route('/materi/emosi-gabungan')
def materi_emosi_gabungan():
    list_nama_emosi =  Materi.query.filter_by(jenis_emosi=2).all()
    return render_template('materi/materi-emosi-gabungan.html', 
                               list_nama_emosi=list_nama_emosi
                               )

@app.route('/materi/emosi-dasar/<emosi>')
def materi_emosi(emosi):
    emosi = emosi.capitalize()
    materi = Materi.query.filter_by(nama_emosi=emosi)
    return render_template('materi/materi-emosi.html', emosi=emosi, materi=materi)

@app.route('/latihan')
def latihan():
    return render_template('latihan/latihan.html')

@app.route('/latihan/<jenisEmosi>/rombel')
def latihan_jenis_emosi(jenisEmosi):
    jenisEmosi_split = jenisEmosi.split('-')[1] 
    session['jenisEmosi'] = jenisEmosi_split.capitalize()
    rombel = Rombel.query.all()
    
    if jenisEmosi == 'emosi-dasar':
        return render_template('latihan/latihan-emosi-dasar.html', rombel=rombel, jenisEmosi=jenisEmosi)
    else:
        return render_template('latihan/latihan-emosi-gabungan.html', rombel=rombel, jenisEmosi=jenisEmosi)

@app.route('/latihan/<jenisEmosi>/rombel/<rombongan>')
def latihan_rombel(jenisEmosi, rombongan):
    session['rombongan'] = rombongan
    jenisEmosiSplit = jenisEmosi.split('-')[1].capitalize()
    jenisEmosi = jenisEmosi 
    users = User.query.filter_by(rombel_id=rombongan).all()
    
    if jenisEmosi == 'emosi-dasar':
        return render_template('latihan/latihan-pemilihan-user.html',
                               users=users, 
                               rombongan=rombongan,
                               jenisEmosi=jenisEmosi,
                               jenisEmosiSplit=jenisEmosiSplit)
    else:
        return render_template('latihan/latihan-pemilihan-user.html',
                               users=users, rombongan=rombongan,
                               jenisEmosi=jenisEmosi,
                               jenisEmosiSplit=jenisEmosiSplit)

@app.route('/latihan/<jenisEmosi>/rombel/<rombongan>/<user>')
def latihan_pilih_emosi(user, rombongan, jenisEmosi):
    session['user'] = user.capitalize()
    jenisEmosiSplit = jenisEmosi.split('-')[1].capitalize()
    jenisEmosi = jenisEmosi 

    if jenisEmosi == 'emosi-dasar':
        jenisLatihan =  Materi.query.filter_by(jenis_emosi=1).all()
        return render_template('latihan/latihan-pemilihan-emosi.html', 
                               rombongan=rombongan,
                               jenisLatihan=jenisLatihan,
                               jenisEmosi=jenisEmosi,
                               jenisEmosiSplit=jenisEmosiSplit
                               )
    else:
        jenisLatihan =  Materi.query.filter_by(jenis_emosi=2).all()
        return render_template('latihan/latihan-pemilihan-emosi.html',
                               rombongan=rombongan,
                               jenisLatihan=jenisLatihan,
                               jenisEmosiSplit=jenisEmosiSplit,
                               jenisEmosi=jenisEmosi)
    
@app.route('/latihan/emosi-dasar/rombel/<rombongan>/<user>/<emosi>')
def latihan_emosi(user, rombongan, emosi):
    session['emosi'] = emosi.capitalize()

    return render_template('latihan/latihan-rombel-dasar-emosi.html')

@app.route('/laporan/rombel')
def laporan_pilih_rombel():
    rombel = Rombel.query.all()
    return render_template('laporan/laporan-pemilihan-rombel.html', rombel=rombel)
    

@app.route('/laporan/rombel/<rombongan>')
def laporan_pilih_user(rombongan):
    session['rombongan'] = rombongan 
    users = User.query.filter_by(rombel_id=rombongan).all()
    
    return render_template('laporan/laporan-pemilihan-user.html',
                               users=users, rombongan=rombongan)



@app.route('/laporan/rombel/<rombongan>/<user>')
def laporan_hasil(user, rombongan):
    # session['user'] = user.capitalize()

    # laporan-dasar =  Materi.query.filter_by(jenis_emosi=1).all()
    # laporan-gabungan =  Materi.query.filter_by(jenis_emosi=2).all()

    return render_template('laporan/laporan-hasil.html',
                               rombongan=rombongan)  

if __name__ == '__main__':
    app.run(debug=True)