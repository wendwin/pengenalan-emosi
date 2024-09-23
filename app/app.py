from flask import Flask,render_template, session, request, redirect, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
import random
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
    
class Laporan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user = db.Column(db.String(50))
    jenis_emosi = db.Column(db.String(50))
    nama_emosi = db.Column(db.String(50))
    status = db.Column(db.String(50))

    def __repr__(self):
        return f'<Laporan {self.id} - {self.jenis_emosi} - {self.nama_emosi} - {self.status}>'

    


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

@app.route('/latihan/<jenisEmosi>/rombel/<rombongan>/<user>', methods=['GET', 'POST'])
def latihan_pilih_emosi(user, rombongan, jenisEmosi):
    session['user'] = user
    jenisEmosiSplit = jenisEmosi.split('-')[1].capitalize()
    jenisEmosi = jenisEmosi
    user = session['user']

    if request.method == 'POST':
        statuslatihan=request.form['statuslatihan']
    
        emosi = session.get('emosi').capitalize()
    

        list_latihanemosi = session.get('list_latihanemosi', [])
        if emosi not in list_latihanemosi:
            list_latihanemosi.append(emosi)
            session['list_latihanemosi'] = list_latihanemosi
            
        if jenisEmosi == 'emosi-dasar':
            if len(list_latihanemosi) == 6:
                laporan = Laporan.query.filter_by(
                    user=user,
                    jenis_emosi=jenisEmosi,
                    nama_emosi=emosi
                ).first()

                if laporan:
                    if Laporan.status != 'berhasil':
                        Laporan.status = 'berhasil'
                        db.session.commit()  
                    else:
                        pass
                else:
                    new_laporan = Laporan(
                        user=user,
                        jenis_emosi=jenisEmosi,
                        nama_emosi=emosi,
                        status=statuslatihan
                    )
                    db.session.add(new_laporan)
                    db.session.commit()

                session.pop('list_latihanemosi')
                session.pop('rombongan')
                session.pop('emosi')
                session.pop('jenisEmosi')
                session.pop('user')
                return redirect(url_for('index'))
            else:
                laporan = Laporan.query.filter_by(
                    user=user,
                    jenis_emosi=jenisEmosi,
                    nama_emosi=emosi
                ).first()

                if laporan:
                    if Laporan.status != 'berhasil':
                        Laporan.status = 'berhasil'
                        db.session.commit()  
                    else:
                        pass
                else:
                    new_laporan = Laporan(
                        user=user,
                        jenis_emosi=jenisEmosi,
                        nama_emosi=emosi,
                        status=statuslatihan
                    )
                    db.session.add(new_laporan)
                    db.session.commit()
                    print(new_laporan.id) 
            jenisLatihan =  Materi.query.filter_by(jenis_emosi=1).all()
            return render_template('latihan/latihan-pemilihan-emosi.html', 
                                   rombongan=rombongan,
                                   jenisLatihan=jenisLatihan,
                                   jenisEmosi=jenisEmosi,
                                   jenisEmosiSplit=jenisEmosiSplit,
                                   user=user,
                                   list_latihanemosi=list_latihanemosi
                                   )                                   
        else:
            if len(list_latihanemosi) == 3:
                laporan = Laporan.query.filter_by(
                    user=user,
                    # rombongan=rombongan,
                    jenis_emosi=jenisEmosi,
                    nama_emosi=emosi
                ).first()

                if laporan:
                    if Laporan.status != 'berhasil':
                        Laporan.status = 'berhasil'
                        db.session.commit()  
                    else:
                        pass
                else:
                    new_laporan = Laporan(
                        user=user,
                        # rombongan=rombongan,
                        jenis_emosi=jenisEmosi,
                        nama_emosi=emosi,
                        status=statuslatihan
                    )
                    db.session.add(new_laporan)
                    db.session.commit()

                session.pop('list_latihanemosi')
                session.pop('rombongan')
                session.pop('namaemosi')
                session.pop('jenisemosi')
                session.pop('siswa')
                return render_template('index.html')
            else:
                laporan = Laporan.query.filter_by(
                    user=user,
                    # rombongan=rombongan,
                    jenis_emosi=jenisEmosi,
                    nama_emosi=emosi
                    ).first()

                if laporan:
                    if Laporan.status != 'berhasil':
                        Laporan.status = 'berhasil'
                        db.session.commit()  
                    else:
                        pass
                else:
                    new_laporan = laporan(
                        user=user,
                        # rombongan=rombongan,
                        jenis_emosi=jenisEmosi,
                        nama_emosi=emosi,
                        status=statuslatihan
                    )
                    db.session.add(new_laporan)
                    db.session.commit()
            jenisLatihan =  Materi.query.filter_by(jenis_emosi=2).all()
            return render_template('latihan/latihan-pemilihan-emosi.html',
                               rombongan=rombongan,
                               jenisLatihan=jenisLatihan,
                               jenisEmosiSplit=jenisEmosiSplit,
                               jenisEmosi=jenisEmosi,
                               user=user,
                               list_latihanemosi=list_latihanemosi)
    else:
        if jenisEmosi == 'emosi-dasar':
            jenisLatihan =  Materi.query.filter_by(jenis_emosi=1).all()
            return render_template('latihan/latihan-pemilihan-emosi.html', 
                                   rombongan=rombongan,
                                   jenisLatihan=jenisLatihan,
                                   jenisEmosi=jenisEmosi,
                                   jenisEmosiSplit=jenisEmosiSplit,
                                   user=user
                                   )
        else:
            jenisLatihan =  Materi.query.filter_by(jenis_emosi=2).all()
            return render_template('latihan/latihan-pemilihan-emosi.html',
                               rombongan=rombongan,
                               jenisLatihan=jenisLatihan,
                               jenisEmosiSplit=jenisEmosiSplit,
                               jenisEmosi=jenisEmosi,
                               user=user)
    
@app.route('/latihan/<jenisEmosi>/rombel/<rombongan>/<user>/<emosi>')
def latihan_emosi(jenisEmosi, user, rombongan, emosi):
    session['emosi'] = emosi
    urlJenisEmosi = jenisEmosi
    jenisEmosi = session['jenisEmosi']
    rombongan = session['rombongan']
    emosi = session['emosi'].capitalize()

    data = {
        'jenis_emosi': jenisEmosi,
        'emosi': emosi
    }

    pilihan_emosi = Materi.query.filter_by(nama_emosi=emosi).first()

    list_emosi = []

    if pilihan_emosi:
        list_emosi.append({
            'nama_emosi': pilihan_emosi.nama_emosi,
            'jenis_emosi': pilihan_emosi.jenis_emosi_rel.jenis,
            'gambar_emosi': pilihan_emosi.gambar_satu
        })
        list_emosi.append({
            'nama_emosi': pilihan_emosi.nama_emosi,
            'jenis_emosi': pilihan_emosi.jenis_emosi_rel.jenis,
            'gambar_emosi': pilihan_emosi.gambar_satu
        })

    data_random = Materi.query.join(JenisEmosi, Materi.jenis_emosi == JenisEmosi.id).filter(
    (Materi.nama_emosi != emosi) & (JenisEmosi.jenis == jenisEmosi)
    ).all()
    random.shuffle(data_random)


    if len(data_random) >= 2:
        random_emosi = random.sample(data_random, 2)
        for item in random_emosi:
            list_emosi.append({
                'nama_emosi': item.nama_emosi,
                'jenis_emosi': item.jenis_emosi_rel.jenis,
                'gambar_emosi': item.gambar_satu
            })
            list_emosi.append({
                'nama_emosi': item.nama_emosi,
                'jenis_emosi': item.jenis_emosi_rel.jenis,
                'gambar_emosi': item.gambar_satu
            })
    else:
        for item in data_random:
            list_emosi.append({
                'nama_emosi': item.nama_emosi,
                'jenis_emosi': item.jenis_emosi_rel.jenis,
                'gambar_emosi': item.gambar_satu
            })
            list_emosi.append({
                'nama_emosi': item.nama_emosi,
                'jenis_emosi': item.jenis_emosi_rel.jenis,
                'gambar_emosi': item.gambar_satu
            })

    random.shuffle(list_emosi)
    
    if jenisEmosi == 'emosi-gabungan':
        if emosi == 'bingung':
            list_emosi_gabungan = []
            pilihan_emosi1 = Materi.query.filter_by(nama_emosi='terkejut').first()
            if pilihan_emosi1:
                list_emosi_gabungan.append({
                    'nama_emosi': pilihan_emosi1.nama_emosi,
                    'jenis_emosi': pilihan_emosi1.jenis_emosi,
                    'gambar_emosi': pilihan_emosi1.gambar_satu
                })
            pilihan_emosi1 = Materi.query.filter_by(nama_emosi='sedih').first()
            if pilihan_emosi1:
                list_emosi_gabungan.append({
                    'nama_emosi': pilihan_emosi1.nama_emosi,
                    'jenis_emosi': pilihan_emosi1.jenis_emosi,
                    'gambar_emosi': pilihan_emosi1.gambar_satu
                })
        elif emosi == 'benci':
            list_emosi_gabungan = []
            pilihan_emosi1 = Materi.query.filter_by(nama_emosi='marah').first()
            if pilihan_emosi1:
                list_emosi_gabungan.append({
                    'nama_emosi': pilihan_emosi1.nama_emosi,
                    'jenis_emosi': pilihan_emosi1.jenis_emosi,
                    'gambar_emosi': pilihan_emosi1.gambar_satu
                })
            pilihan_emosi1 = Materi.query.filter_by(nama_emosi='takut').first()
            if pilihan_emosi1:
                list_emosi_gabungan.append({
                    'nama_emosi': pilihan_emosi1.nama_emosi,
                    'jenis_emosi': pilihan_emosi1.jenis_emosi,
                    'gambar_emosi': pilihan_emosi1.gambar_satu
                })
        elif emosi == 'kagum':
            list_emosi_gabungan = []
            pilihan_emosi1 = Materi.query.filter_by(nama_emosi='terkejut').first()
            if pilihan_emosi1:
                list_emosi_gabungan.append({
                    'nama_emosi': pilihan_emosi1.nama_emosi,
                    'jenis_emosi': pilihan_emosi1.jenis_emosi,
                    'gambar_emosi': pilihan_emosi1.gambar_satu
                })
            pilihan_emosi1 = Materi.query.filter_by(nama_emosi='takut').first()
            if pilihan_emosi1:
                list_emosi_gabungan.append({
                    'nama_emosi': pilihan_emosi1.nama_emosi,
                    'jenis_emosi': pilihan_emosi1.jenis_emosi,
                    'gambar_emosi': pilihan_emosi1.gambar_satu
                })

        return render_template('latihan/latihan-emosi.html',
                           emosi=emosi,
                           user=user,
                           jenisEmosi=jenisEmosi,
                           rombongan=rombongan,
                           list_emosi=list_emosi,
                           list_emosi_gabungan=list_emosi_gabungan,
                           urlJenisEmosi=urlJenisEmosi,
                           data=data
                           )    
    return render_template('latihan/latihan-emosi.html',
                           emosi=emosi,
                           user=user,
                           jenisEmosi=jenisEmosi,
                           rombongan=rombongan,
                           list_emosi=list_emosi,
                           urlJenisEmosi=urlJenisEmosi,
                           data=data
                           )    
    

if __name__ == '__main__':
    app.run(debug=True)