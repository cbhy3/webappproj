from flask import Flask, render_template, redirect, request, redirect, url_for
from Forms import *
import shelve as shelve
from customer import Customer
from currentUser import CurrentUser
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
    current_user = None
    signinform = signIn()
    signupform = signUp()
    if request.method == 'POST':
        # Distinguish between forms
        if 'signin_submit' in request.form and signinform.validate_on_submit():
            siemail = signinform.email.data
            sipassword = signinform.password.data
            print("Sign-in attempt:", siemail)
            with shelve.open('users') as usersDB:
                current_user = usersDB[siemail]
                ##print(current_user)
        elif 'signup_submit' in request.form and signupform.validate_on_submit():
            suemail = signupform.email.data
            supassword = signupform.password.data
            print("Sign-up attempt:", suemail)
            Customer(suemail, supassword)
            return redirect(url_for('about_us'))
        else:
            print("Form validation failed:", signupform.errors, signinform.errors)

    return render_template('aboutus.html', active_page='aboutus', signinform=signinform, signupform=signupform, siemail=siemail,sipassword=sipassword,suemail=suemail,supassword=supassword, current_user=current_user)
## copy this shit into the other pages when finished making them
@app.route('/catalog')
def catalog():
    return render_template('index.html', active_page='catalog')

@app.route('/cart')
def cart():
    return render_template('index.html', active_page='cart')
if __name__ == '__main__':
    app.run(debug=True)
