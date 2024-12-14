from flask import Flask, render_template, redirect, request, redirect, url_for
from Forms import *
import shelve as shelve
from customer import Customer
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bignuts'

@app.route('/')
def main():
    return redirect('/aboutus')

@app.route('/aboutus', methods=['GET', 'POST'])
def about_us():
    siemail = None
    sipassword = None
    suemail = None
    supassword = None
    signinform = signIn()
    signupform = signUp()
    if signinform.validate_on_submit():
        siemail = signinform.email.data
        sipassword = signinform.password.data
        ## have not made sign in validation
    if signupform.validate_on_submit():
        suemail = signupform.email.data
        supassword = signupform.password.data
        Customer(suemail,supassword)
        return redirect(url_for('about_us'))

    return render_template('aboutus.html', active_page='aboutus', signinform=signinform, signupform=signupform, siemail=siemail,sipassword=sipassword,suemail=suemail,supassword=supassword)

@app.route('/catalog')
def catalog():
    return render_template('index.html', active_page='catalog')

@app.route('/cart')
def cart():
    return render_template('index.html', active_page='cart')
if __name__ == '__main__':
    app.run(debug=True)
