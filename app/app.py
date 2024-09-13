from flask import Flask,render_template, session, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import random



app = Flask(__name__)
app.config['SECRET_KEY'] = '1234567890'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/emoji'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class siswa(db.Model):
    nama = db.Column(db.String(20), primary_key=True)
    rombongan = db.Column(db.Integer, primary_key=True)

class laporan(db.Model):
    nama = db.Column(db.String(20), primary_key=True)
    rombongan = db.Column(db.Integer, primary_key=True)
    jenisemosi = db.Column(db.String(20), primary_key=True)
    namaemosi = db.Column(db.String(20), primary_key=True)
    statuslatihan = db.Column(db.String(20), primary_key=True)

@app.route('/laporan/rombongan')
def laporanrombongan():
    return render_template('laporanrombongan.html')

@app.route('/laporan/rombongan/siswa', methods=["POST"])
def laporannamasiswa():
    rombongan=request.form['rombongan']
    rombongan=int(rombongan)
    session['rombongan']=rombongan
    if rombongan == 1:
        hasil = siswa.query.filter_by(rombongan=1).all()
        nama_list = [siswa.nama for siswa in hasil]
        return render_template('laporansiswa.html',nama_list=nama_list, rombongan=rombongan)

@app.route('/laporan/rombongan/siswa/hasil', methods=["POST"])
def hasillaporan():
    nama=request.form['siswa']
    rombongan=session['rombongan']
    jenisemosidasar='dasar'
    jenisemosigabungan='gabungan'
    if nama and rombongan:
        hasil = laporan.query.filter_by(nama=nama, rombongan=rombongan, jenisemosi=jenisemosidasar).all()
        list_statuslatihandasar = [laporan for laporan in hasil]
        return render_template('hasillaporan.html',list_statuslatihandasar=list_statuslatihandasar, rombongan=rombongan, nama=nama, jenisemosidasar=jenisemosidasar)

if __name__ == '__main__':
    app.run(debug=True)