from flask import Flask, render_template, redirect

app = Flask(__name__)


@app.route('/')
def main():
    return redirect('/aboutus')

@app.route('/aboutus')
def about_us():
    return render_template('aboutus.html', active_page='aboutus')

@app.route('/catalog')
def catalog():
    return render_template('index.html', active_page='catalog')


@app.route('/cart')
def cart():
    return render_template('index.html', active_page='cart')
if __name__ == '__main__':
    app.run(debug=True)
