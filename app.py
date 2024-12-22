from flask import Flask, render_template, redirect, request, redirect, url_for, session
from Forms import *
import shelve as shelve
from customer import Customer
from currentUser import CurrentUser
from generateOTP import generateOTP
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bignuts'

@app.route('/')
def main():
    return redirect('/aboutus')

@app.route('/aboutus', methods=['GET', 'POST'])
def about_us():
    with shelve.open('users') as db:
        for i in db:
            del db[i]
    siemail = None
    sipassword = None
    suemail = None
    supassword = None
    current_user = None
    signinform = signIn()
    signupform = signUp()
    otpform = Otp()
    needOTP = False
    registrationSuccessful = False
    signup = False
    if request.method == 'POST':
        # Distinguish between forms
        if 'signin_submit' in request.form and signinform.validate_on_submit():
            siemail = signinform.email.data
            sipassword = signinform.password.data
            print("Sign-in attempt:", siemail)
            registrationSuccessful = False
            with shelve.open('users') as usersDB:
                current_user = usersDB[siemail]
                ##print(current_user)
        elif 'signup_submit' in request.form and signupform.validate_on_submit():
            suemail = signupform.email.data
            supassword = signupform.password.data
            session['user_email'] = suemail
            session['user_password'] = supassword
            print("Sign-up attempt:", suemail)
            needOTP = True
            otp = generateOTP.__call__(suemail)
            session['otp'] = otp
            print(session['otp'])
        elif 'otp_submit' in request.form and otpform.validate_on_submit():
            registrationSuccessful = True
            print("registration successful")
            Customer(session.get('user_email'), session.get('user_password'))
        elif 'new_email_submit' in request.form:
            needOTP = False
            signup = True
        else:
            print("Form validation failed:", signupform.errors, signinform.errors, otpform.errors)

    return render_template('aboutus.html', active_page='aboutus', signinform=signinform, signupform=signupform, siemail=siemail,sipassword=sipassword,suemail=suemail,supassword=supassword, current_user=current_user, needOTP=needOTP, otpform=otpform, registrationSuccessful=registrationSuccessful, signup=signup)
## copy this shit into the other pages when finished making them
@app.route('/catalog')
def catalog():
    return render_template('index.html', active_page='catalog')

@app.route('/cart')
def cart():
    return render_template('index.html', active_page='cart')
if __name__ == '__main__':
    app.run(debug=True)
