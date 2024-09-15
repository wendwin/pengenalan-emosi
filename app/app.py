from flask import Flask,render_template, session, request, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KaVGm31asLwNAlaoG'

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
    return render_template('latihan/latihan-emosi-dasar.html')

@app.route('/latihan/rombel/emosi-gabungan')
def latihan_rombel_gabungan():
    return render_template('latihan/latihan-emosi-gabungan.html')

if __name__ == '__main__':
    app.run(debug=True)