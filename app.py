from flask import Flask, render_template, redirect, request, redirect, url_for, session, jsonify
from Forms import *
import shelve as shelve
from customer import Customer
from currentUser import CurrentUser
from generateOTP import generateOTP, generateOTPforReset
from manager import Manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'bignuts'
@app.route('/')
def main():
    return redirect('/aboutus')

@app.route('/aboutus', methods=['GET', 'POST'])
def about_us():
    #with shelve.open('users') as db:
      #  for i in db:
        #   del db[i]                  ## clear user db for testing
    #with shelve.open('admin') as db:
      # for i in db:
        #   del db[i]

    siemail = None
    sipassword = None
    suemail = None
    supassword = None
    try:
        current_user = CurrentUser.fromEmail(session.get('current_user'))
    except:
        current_user = None
    needresetemail = False
    signinform = signIn()
    signupform = signUp()
    otpform = Otp()
    resetpasswordemail = resetPasswordEmail()
    resetPasswordotp = resetPasswordOTP()
    resetpassword = resetPassword()

    needOTP = False
    registrationSuccessful = False
    signup = False
    needresetpasswordotp = False
    needresetpassword = False
    resetsuccessful = False
    if request.method == 'POST':
        # Distinguish between forms
        if 'signin_submit' in request.form and signinform.validate_on_submit():
            needresetemail = False
            siemail = signinform.email.data
            sipassword = signinform.password.data
            print("Sign-in attempt:", siemail)
            registrationSuccessful = False
            with shelve.open('users') as usersDB:
                current_user = usersDB[siemail]
                ##print(current_user)
            session['current_user'] = current_user.getEmail()
            session.permanent = True
        elif 'forgotpass_submit' in request.form:
            needresetemail = True
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
            needOTP = False
            print("registration successful")
            Customer(session.get('user_email'), session.get('user_password'))
            session.pop('user_email')
            session.pop('user_password')
            session.pop('otp')
        elif 'new_email_submit' in request.form:
            needOTP = False
            signup = True
        elif 'reset_password_email_submit' in request.form and resetpasswordemail.validate_on_submit():
            resetemail = resetpasswordemail.email.data
            resetotp = generateOTPforReset.__call__(resetemail)
            session['resetotp'] = resetotp
            session['email'] = resetemail
            print(session['resetotp'])
            needresetemail = False
            needresetpasswordotp = True
        elif 'resetpasswordotp_submit' in request.form and resetPasswordotp.validate_on_submit():
            needresetpasswordotp = False
            needresetpassword = True
            session.pop('resetotp')
            with shelve.open('users') as usersDB:
                session['oldPassword'] = usersDB[session['email']].password
        elif 'reset_password_submit' in request.form and resetpassword.validate_on_submit():
            with shelve.open('users') as usersDB:
                u = usersDB[session['email']]
                u.setPassword(resetpassword.password.data)
                usersDB[session['email']] = u
                print(u)
            resetsuccessful = True
            session.pop('oldPassword')
            session.pop('email')
        else:
            print("Form validation failed:", signupform.errors, signinform.errors, otpform.errors)

    return render_template('aboutus.html', active_page='aboutus', signinform=signinform,
                           signupform=signupform, siemail=siemail,sipassword=sipassword,suemail=suemail,supassword=supassword,
                           current_user=current_user, needOTP=needOTP, otpform=otpform, registrationSuccessful=registrationSuccessful,
                           signup=signup, resetPasswordOTP = resetPasswordotp, needresetemail = needresetemail, resetpasswordemail = resetpasswordemail,
                           needresetpasswordotp = needresetpasswordotp, needresetpassword = needresetpassword, resetpassword = resetpassword, resetsuccessful=resetsuccessful,)
## copy this shit into the other pages when finished making them
@app.route('/catalog')
def catalog():
    return render_template('index.html', active_page='catalog')

@app.route('/cart')
def cart():
    return render_template('index.html', active_page='cart')
if __name__ == '__main__':
    app.run(debug=True)
current_tab = 'profile'
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    siemail = None
    sipassword = None
    suemail = None
    supassword = None
    global current_tab
    print(current_tab)
    try:
        current_user = CurrentUser.fromEmail(session.get('current_user'))
    except KeyError:
        current_user = None
    needresetemail = False
    signinform = signIn()
    signupform = signUp()
    otpform = Otp()
    resetpasswordemail = resetPasswordEmail()
    resetPasswordotp = resetPasswordOTP()
    resetpassword = resetPassword()

    needOTP = False
    registrationSuccessful = False
    signup = False
    needresetpasswordotp = False
    needresetpassword = False
    resetsuccessful = False
    signoutform  = signOut()
    change_email = changeEmail()
    change_emailEmail = None
    if request.method == 'POST':

        if 'signout_submit' in request.form and signoutform.validate_on_submit():
            current_user = None
            session.pop('current_user')
            return redirect(url_for('about_us'))
        elif 'signout_cancel_submit' in request.form and signoutform.validate_on_submit():
            pass
        elif 'change_email_submit' in request.form and change_email.validate_on_submit():
            change_emailEmail = change_email.email.data
            needOTP = True
            otp = generateOTP.__call__(change_emailEmail)
            session['otp'] = otp
            print(session['otp'])
            session.pop('otp')
            if 'otp_submit' in request.form and otpform.validate_on_submit():
                with shelve.open('users') as usersDB:
                    usersDB[session.get('current_user')].setEmail(change_emailEmail)
                needOTP = False
            ## add functionality for using a different email in the html, like similiar to the one in the signup
        else:
            print("Form validation failed:",)
    if current_user is None:
        return redirect(url_for('about_us'))
    return render_template('profile.html', active_page='profile',signoutform = signoutform, current_tab = current_tab,signinform=signinform,
                           signupform=signupform, siemail=siemail,sipassword=sipassword,suemail=suemail,supassword=supassword,
                           current_user=current_user, needOTP=needOTP, otpform=otpform, registrationSuccessful=registrationSuccessful,
                           signup=signup, resetPasswordOTP = resetPasswordotp, needresetemail = needresetemail, resetpasswordemail = resetpasswordemail,
                           needresetpasswordotp = needresetpasswordotp, needresetpassword = needresetpassword, resetpassword = resetpassword, resetsuccessful=resetsuccessful,)

@app.route('/updatep', methods = ['POST'])
def update_profile_tab():
    global current_tab
    tab = request.json
    new_tab = tab.get('new_tab')
    if new_tab:
        current_tab = new_tab
        return jsonify(current_tab)
    return jsonify("eat dog"), 400
@app.route('/admin', methods=['GET', 'POST'])
def Admin():
    try:
        current_user = User.fromJSON(session['current_user'])
        with shelve.open('admin') as adminDB:
            isAdmin = adminDB[current_user.email]
    except:
        redirect(url_for('about_us'))
    return render_template('admin.html')