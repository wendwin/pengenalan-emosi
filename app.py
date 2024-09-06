from flask import Flask,render_template, session, request, redirect, url_for

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234567890'

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


if __name__ == '__main__':
    app.run(debug=True)