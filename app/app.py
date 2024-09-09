from flask import Flask,render_template, session, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    css = 'beranda.css'
    return render_template('home.html', css=css)

@app.route('/materi')
def materi():
    return render_template('materi.html')

@app.route('/latihan')
def latihan():
    return render_template('latihan.html')

@app.route('/laporan/rombongan')
def laporanrombongan():
    return render_template('laporanrombongan.html')


if __name__ == '__main__':
    app.run(debug=True)