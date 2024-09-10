from flask import Flask,render_template, session, request, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = 'KaVGm31asLwNAlaoG'

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
    return render_template('materi/materi-emosi-dasar.html')

@app.route('/materi/emosi-gabungan')
def materi_emosi_gabungan():
    return render_template('materi/materi-emosi-gabungan.html')

@app.route('/latihan')
def latihan():
    return render_template('latihan/latihan.html')

@app.route('/latihan/rombel', methods=["POST"])
def latihan_rombel():
    jenisEmosi=request.form['jenisEmosi']
    session['jenisEmosi']=jenisEmosi
    return render_template('latihan/latihan-emosi.html', jenisemosi=jenisEmosi)


if __name__ == '__main__':
    app.run(debug=True)