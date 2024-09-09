from flask import Flask,render_template, session, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    css = 'beranda.css' 
    return render_template('home.html', css=css)

@app.route('/materi')
def materi():
    css = 'beranda.css'
    return render_template('materi/materi.html', css=css)

@app.route('/materi/emosi-dasar')
def materi_emosi_dasar():
    return render_template('materiemosidasar.html')

@app.route('/materi/emosi-gabungan')
def materi_emosi_gabungan():
    return render_template('materiemosigabungan.html')

@app.route('/latihan')
def latihan():
    return render_template('latihan.html')

@app.route('/laporan/rombongan')
def laporan_rombongan():
    return render_template('laporanrombongan.html')


if __name__ == '__main__':
    app.run(debug=True)