from flask import Flask,render_template, session, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config['SECRET_KEY'] = '1234567890'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/emoji'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class siswa(db.Model):
    nama = db.Column(db.String(20), primary_key=True)
    rombongan = db.Column(db.Integer, primary_key=True)

@app.route('/')
def index():
    return render_template('beranda.html')

@app.route('/materi')
def materi():
    return render_template('materi.html')

@app.route('/materi/emosidasar')
def materiemosidasar():
    return render_template('materiemosidasar.html')

@app.route('/materi/emosigabungan')
def materiemosigabungan():
    return render_template('materiemosigabungan.html')

@app.route('/latihan')
def latihan():
    return render_template('latihan.html')

@app.route('/latihan/rombongan', methods=["POST"])
def latihanrombongan():
    jenisemosi=request.form['jenisemosi']
    session['jenisemosi']=jenisemosi
    return render_template('latihanrombongan.html',jenisemosi=jenisemosi)

    
@app.route('/latihan/rombongan/siswa', methods=["POST"])
def namasiswa():
    jenisemosi=session['jenisemosi']
    rombongan=request.form['rombongan']
    rombongan=int(rombongan)
    if rombongan == 1:
        hasil = siswa.query.filter_by(rombongan=1).all()
        nama_list = [siswa.nama for siswa in hasil]
        return render_template('latihansiswa.html',nama_list=nama_list, rombongan=rombongan,jenisemosi=jenisemosi)
        
@app.route('/latihan/rombongan/siswa/cihuy', methods=["POST"])
def namaemosi():
    siswa=request.form['siswa']
    jenisemosi=session['jenisemosi']
    return render_template('latihannamaemosi.html', jenisemosi=jenisemosi)


if __name__ == '__main__':
    app.run(debug=True)