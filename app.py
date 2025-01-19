from flask import Flask, render_template, redirect, request, redirect, url_for, session, jsonify
from Forms import *
import shelve as shelve
from customer import Customer
from currentUser import CurrentUser
from generateOTP import generateOTP, generateOTPforReset
from Product import Product
from manager import Manager
import copy
import datetime
import threading
import time
app = Flask(__name__)
app.config['SECRET_KEY'] = 'bignuts'



def updateCooldown():
    while True:
        try:
            with shelve.open('users', writeback=True) as usersDB:
                for user_key in usersDB:
                    user = usersDB[user_key]
                    if user.Cooldown > 0:
                        user.decreaseCooldown()


        except Exception as e:
            print(f"Error: {e}")
        time.sleep(1)

thread = threading.Thread(target=updateCooldown, daemon=True)
thread.start()
print("thread started")

if __name__ == '__main__':

    app.run(debug=True)
@app.route('/')
def main():
    return redirect('/aboutus')

login = "SignIn"
@app.route('/sign_in', methods = ['GET', 'POST'])
def sign_in():
    try:
        current_user = CurrentUser.fromEmail(session.get('current_user'))
        return redirect(url_for('about_us'))
    except:
        current_user = None
    global login
    sign_in_form = signIn()
    sign_up_form = signUp()
    reset_password_email = resetPasswordEmail()
    reset_password_otp = resetPasswordOTP()
    reset_password = resetPassword()
    otp_form = Otp()

    if request.method == 'POST':
        if 'signin_submit' in request.form and sign_in_form.validate_on_submit() :
            print("sign in attempt, ", sign_in_form.email.data)
            with shelve.open('users') as usersDB:
                current_user = usersDB[sign_in_form.email.data]
                print(current_user.getEmail())
            session['current_user'] = current_user.getEmail()
            session.permanent = True
            return redirect(url_for('about_us'))
        elif 'signup_submit' in request.form and sign_up_form.validate_on_submit() :
            session["sign_up_email"] = sign_up_form.email.data
            session["sign_up_password"] = sign_up_form.password.data
            email = session['sign_up_email']
            login = "OTP"
            otp = generateOTP().__call__(email)
            session["otp"] = otp
            print(otp)
            return redirect(url_for('sign_in'))
        elif 'otp_submit' in request.form and otp_form.validate_on_submit() :
            Customer(session.get('sign_up_email'), session.get('sign_up_password'))
            session['current_user'] = session.get('sign_up_email')
            session.permanent = True
            session.pop('sign_up_email')
            session.pop('sign_up_password')
            return redirect(url_for('about_us'))
        elif 'reset_password_email_submit' in request.form and reset_password_email.validate_on_submit() :
            login = "ResetPasswordOtp"
            reset_email = reset_password_email.email.data
            otp = generateOTPforReset().__call__(reset_email)
            session["resetotp"] = otp
            session["reset_email"] = reset_email
            print(otp)
            return redirect(url_for('sign_in'))
        elif "resetpasswordotp_submit" in request.form and reset_password_otp.validate_on_submit() :
            login = "ResetPassword"
            with shelve.open('users') as usersDB:
                session['oldPassword'] = usersDB[session['reset_email']].password
            return redirect(url_for('sign_in'))
        elif 'reset_password_submit' in request.form and reset_password.validate_on_submit():
            with shelve.open('users') as usersDB:
                u = usersDB[session['reset_email']]
                u.setPassword(reset_password.password.data)
                usersDB[session['reset_email']] = u
            session.pop('reset_email')
            login = "SignIn"
            return redirect(url_for('sign_in'))
        else:
            sign_in_form.email.data = ""
            sign_in_form.password.data = ""
            sign_up_form.password.data = ""
            sign_up_form.email.data = ""
            otp_form.otp.data = ""
            reset_password_email.email.data = ""
            reset_password_otp.otp.data = ""
            reset_password.password.data = ""
            reset_password.verifypassword.data = ""
            print("something went wrong somewhere")

    return render_template('signin.html', sign_in_form = sign_in_form, sign_up_form = sign_up_form, reset_password = reset_password, reset_password_otp = reset_password_otp, reset_password_email = reset_password_email, login = login, otp_form = otp_form)

@app.route('/change_login_action', methods = ['GET', 'POST'])
def change_login_action():
    global login
    print(login)
    data = request.json
    new_login = data.get('new_login')
    print(new_login)
    if new_login:
        login = new_login
        print(login)
        return jsonify(login)
    return jsonify("eat dog"), 400
@app.route('/aboutus', methods=['GET', 'POST'])
def about_us():
    #with shelve.open('users') as db:
    #    for i in db:
    #        del db[i]                  ## clear user db for testing
    #with shelve.open('admin') as db:   # REWRITE EVERYTHING TO DO WITH SIGNING IN AND SIGN UP THIS SHIT IS SO BAD
    #   for i in db:
    #       del db[i]
    with shelve.open('users') as usersDB:
        for i in usersDB:
            print(i)
    cart = None
    try:
        current_user = CurrentUser.fromEmail(session.get('current_user'))
        cart = current_user.Cart
    except:
        current_user = None



    return render_template('aboutus.html', active_page='aboutus',
                           current_user=current_user, cart = cart)
## copy this shit into the other pages when finished making them
@app.route('/catalog', methods=['GET', 'POST'])
def catalog():
    with shelve.open('products') as products:
        all_products = {key: products[key] for key in products}
    with shelve.open('users') as usersDB:
        for i in usersDB:
            print(i)
    cart = None
    try:
        current_user = CurrentUser.fromEmail(session.get('current_user'))
        cart = current_user.Cart
    except:
        current_user = None


    return render_template('catalog.html', active_page='catalog', products=all_products, cart = cart)



current_tab = 'profile'

@app.route('/profile', methods=['GET', 'POST'])
def profile():


    global current_tab
    print(current_tab)
    current_user = None
    cart = None
    codes = None
    cooldown = None
    try:
        current_user = CurrentUser.fromEmail(session.get('current_user'))
        cart = current_user.Cart
        codes = current_user.Codes
        cooldown = current_user.Cooldown
        print(codes)
    except KeyError:
        current_user = None
    otpform = Otp()
    needOTP = False
    signoutform  = signOut()
    change_email = changeEmail()
    change_emailEmail = None
    need_change_email = None
    change_password = changePassword()
    delete_account = deleteAccount()
    if request.method == 'POST' :
        if 'signout_submit' in request.form and signoutform.validate_on_submit():
            current_user = None
            session.pop('current_user')
            return redirect(url_for('about_us'))
        elif 'signout_cancel_submit' in request.form and signoutform.validate_on_submit():
            pass
        elif 'change_email_submit' in request.form and change_email.validate_on_submit():
            change_emailEmail = change_email.email.data
            session['change_email'] = change_emailEmail
            print(change_email.email.data)
            needOTP = True
            otp = generateOTP.__call__(change_emailEmail)
            session['otp'] = otp
            print(session['otp'])
        elif 'otp_submit' in request.form and otpform.validate_on_submit():
            with shelve.open('users') as usersDB:
                temp = copy.deepcopy(usersDB[session.get('current_user')])
                temp.setEmail(session.get('change_email'))
                usersDB[temp.getEmail()] = temp
                del usersDB[session.get('current_user')]
            session['current_user'] = temp.getEmail()
            current_user = temp
            session.pop('change_email')
            needOTP = False
        elif 'new_email_submit' in request.form:
            needOTP = False
            need_change_email = True
        elif 'change_password_submit' in request.form and change_password.validate_on_submit():
            with shelve.open('users') as usersDB:
                temp = copy.deepcopy(usersDB[session.get('current_user')])
                temp.setPassword(change_password.newPassword.data)
                usersDB[temp.getEmail()] = temp
        elif 'delete_submit' in request.form and delete_account.validate_on_submit():
            with shelve.open('users') as usersDB:
                del usersDB[session.get('current_user')]
            current_user = None
            session.pop('current_user')
            return redirect(url_for('about_us'))
        else:
            print("Form validation failed:", otpform.errors, change_email.errors)
    if current_user is None:
        return redirect(url_for('about_us'))
    return render_template('profile.html', active_page='profile',signoutform = signoutform, current_tab = current_tab,
                           current_user=current_user, needOTP=needOTP, otpform=otpform, change_email = change_email,
                           change_emailEmail = change_emailEmail, need_change_email = need_change_email, change_password = change_password, cart = cart, codes = codes, cooldown = cooldown, delete_account = delete_account)

@app.route('/updatep', methods = ['POST'])
def update_profile_tab():
    global current_tab
    tab = request.json
    new_tab = tab.get('new_tab')
    if new_tab:
        current_tab = new_tab
        return jsonify(current_tab)
    return jsonify("eat dog"), 400

action = 'Default'

@app.route('/updateadminaction', methods = ['POST'])
def updateadmin_action():
    global action
    action = request.json
    new_action = action.get('new_action')
    if new_action:
        action = new_action
        return jsonify(action)
    return jsonify("piss off"), 400


@app.route('/admin', methods=['GET', 'POST'])
def Admin():
    try:
        current_user = User.fromJSON(session['current_user'])
        with shelve.open('admin') as adminDB:
            isAdmin = adminDB[current_user.email]
    except:
        redirect(url_for('about_us'))
    add_product = addProduct()
    modify_product = modifyProduct()
    global action
    if request.method == 'POST':
        if add_product.validate_on_submit() and 'add_product_submit' in request.form:
            with shelve.open('products') as productsDB:
                Product(add_product.name.data, add_product.price.data, add_product.quantity.data, add_product.categories.data, add_product.image_url.data, add_product.description.data, add_product.expiry.data, add_product.weight.data)
            print('new product added')
            return redirect(url_for('Admin'))

        elif 'modify_product_submit' in request.form:
            with shelve.open('products') as productsDB:
                if modify_product.name.data:
                    Product.change_name(modify_product.product.data, modify_product.name.data)
                    print('name updated')
                elif modify_product.price.data:
                    Product.change_price(modify_product.product.data, modify_product.price.data)
                    print('price updated')
                elif modify_product.quantity.data:
                    Product.add_quantity(modify_product.product.data, modify_product.quantity.data)
                    print('quantity updated')
                elif modify_product.categories.data:
                    Product.change_categories(modify_product.product.data, modify_product.categories.data)
                    print('categories updated')
                elif modify_product.weight.data:
                    Product.change_weight(modify_product.product.data, modify_product.weight.data)
                    print('weight updated')
                elif modify_product.expiry.data:
                    Product.update_expiry(modify_product.product.data, modify_product.expiry.data)
                    print('expiry updated')
                elif modify_product.description.data:
                    Product.change_description(modify_product.product.data, modify_product.description.data)
                    print('quantity updated')
                elif modify_product.image_url.data:
                    Product.change_image(modify_product.product.data, modify_product.image_url.data)
                    print('image url updated')
                else:
                    print('error somewhere')
                return redirect(url_for('Admin'))
        elif 'delete_submit' in request.form:
            with shelve.open('products') as productsDB:
                Product.remove_product(modify_product.product.data)
            return redirect(url_for('Admin'))
        else:
            print('form validation failed', add_product.errors)
    return render_template('admin.html', add_product = add_product, action=action , modify_product = modify_product)

@app.route('/catalog/product/<int:product_id>', methods = ['GET', 'POST'])
def product_detail(product_id):
    with shelve.open('products') as productsDB:
        product = productsDB[str(product_id)]
        if not product:
            return "Product not found",404
    with shelve.open('users') as usersDB:
        for i in usersDB:
            print(i)
    try:
        current_user = CurrentUser.fromEmail(session.get('current_user'))
        cart = current_user.Cart
    except:
        current_user = None
        cart = None

    return render_template('product_detail.html', product = product,active_page='catalog',
                           current_user=current_user, cart = cart)



@app.route('/catalog/addtocart/<int:product_id>', methods=['GET', 'POST'])
def addtocart(product_id):
    try:
        with shelve.open('users') as usersDB:
            current_user = usersDB[session.get('current_user')]
            current_user.addToCart(product_id)
            for i in current_user.Cart:
                with shelve.open('products') as productsDB:
                    print(f'{productsDB[str(i)]},,,, quantity: {current_user.Cart[i]}')
        return redirect(url_for('catalog'))

    except KeyError as e:
        return redirect(url_for('sign_in'))

@app.route('/catalog/removefromcart/<int:product_id>', methods=['GET', 'POST'])
def removefromcart(product_id):
    with shelve.open('users') as usersDB:
        current_user = usersDB[session.get('current_user')]
        current_user.removeFromCart(product_id)
        for i in current_user.Cart:
            with shelve.open('products') as productsDB:
                print(f'{productsDB[str(i)]},,,, quantity: {current_user.Cart[i]}')
    return redirect(url_for('cart'))

@app.route('/catalog/addtocart_cart/<int:product_id>', methods=['GET', 'POST'])
def addtocart_cart(product_id):
    with shelve.open('users') as usersDB:
        current_user = usersDB[session.get('current_user')]
        current_user.addToCart(product_id)
        for i in current_user.Cart:
            with shelve.open('products') as productsDB:
                print(f'{productsDB[str(i)]},,,, quantity: {current_user.Cart[i]}')
    return redirect(url_for('cart'))
@app.route('/set_signup', methods=['POST'])
def set_signup():
    global signup
    data = request.get_json()
    if 'signup' in data:
        signup = data['signup']
        return jsonify({'message': 'Signup status updated', 'signup': signup}), 200
    return jsonify({'error': 'Invalid data'}), 400

voucherUsed = False
codeUsed = None
discount = None
gifts = None
freeShipping = False
@app.route('/useVoucher/<code>', methods=['POST', 'GET'])
def useVoucher(code):
    with shelve.open('users') as usersDB:
        current_user = usersDB[session.get('current_user')]
    global voucherUsed
    global discount
    global gifts
    global freeShipping
    global codeUsed
    voucherUsed = True
    if code == 'CHOC':
        gifts = 'Complementary Chocolate Bar'
        current_user.removeCode(code)
        codeUsed = code
    elif code == 'TOTE':
        gifts = 'Complementary Tote Bag'
        current_user.removeCode(code)
        codeUsed = code
    elif code == 'SHIP':
        freeShipping = True
        current_user.removeCode(code)
        codeUsed = code
    elif code == '5OFF':
        discount = 5
        current_user.removeCode(code)
        codeUsed = code
    elif code == '10OFF':
        discount = 10
        current_user.removeCode(code)
        codeUsed = code
    elif code == '15OFF':
        discount = 15
        current_user.removeCode(code)
        codeUsed = code
    elif code == '50OFF':
        discount = 50
        current_user.removeCode(code)
        codeUsed = code
    return redirect(url_for('cart'))


@app.route('/removeVoucher/<code>', methods=['POST', 'GET'])
def removeVoucher(code):
    with shelve.open('users') as usersDB:
        current_user = usersDB[session.get('current_user')]
    global voucherUsed
    global discount
    global gifts
    global freeShipping
    global codeUsed
    voucherUsed = False
    discount = None
    gifts = None
    freeShipping = False
    current_user.addCode(code)
    codeUsed = None
    return redirect(url_for('cart'))
@app.route('/cart', methods = ['GET', 'POST'])
def cart():
    try:
        with shelve.open('products') as products:
            all_products = {key: products[key] for key in products}
        with shelve.open('users') as usersDB:
            current_user = usersDB[session.get('current_user')]
            codes = current_user.Codes
        cart = current_user.Cart

        subtotal = 0
        for i in cart:
            subtotal += all_products[str(i)].price * cart.get(i)
        print(subtotal)
        global voucherUsed
        global discount
        global gifts
        global freeShipping
        global codeUsed

        return render_template('cart.html',active_page='cart', products=all_products, cart = cart, subtotal = subtotal, codes = codes, voucherUsed = voucherUsed
                               , discount = discount, gifts = gifts, freeShipping = freeShipping, codeUsed = codeUsed)

    except KeyError as e:
        print(e)
        signup = True
        return redirect(url_for('catalog'))
@app.route('/profile/game', methods = ['GET', 'POST'])
def game():
    try:
        with shelve.open('users') as usersDB:
            current_user = usersDB[session.get('current_user')]
            if current_user.Cooldown != 0:
                return redirect(url_for('profile'))
    except KeyError as e:
        return redirect(url_for('sign_in'))


    return render_template('game.html', active_page='profile',
                           current_user=current_user,)

@app.route('/profile/givevoucher', methods = ['GET','POST'])
def giveVoucher():
    data = request.get_json()
    if not data or 'code' not in data:
        return jsonify({'error': 'Invalid data'}), 400

    code = data['code']
    try:
        with shelve.open('users') as usersDB:
            print(usersDB[session.get('current_user')].Codes[code])
            usersDB[session.get('current_user')].addCode(code)
            usersDB[session.get('current_user')].updateCooldown(10)
            print(usersDB[session.get('current_user')].Codes[code])
    except KeyError as e:
          return jsonify({'error': 'Database error', 'details': str(e)}), 500

    print(code)

    return jsonify({'success': True, 'message': 'Code redeemed successfully'})