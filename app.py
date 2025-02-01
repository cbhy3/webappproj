import base64
import random
import re

from flask import Flask, render_template, redirect, request, redirect, url_for, session, jsonify, send_file
from Forms import *
import shelve as shelve

from Ticket import Ticket
from customer import Customer
from currentUser import CurrentUser
from generateOTP import generateOTP, generateOTPforReset
from Product import Product
from manager import Manager
from Order import Order
import copy
import datetime
import threading
import time
import generatePayNowQR
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
    #with shelve.open('admin') as db:
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


    return render_template('catalog.html', active_page='catalog', products=all_products, cart = cart, current_user = current_user)



current_tab = 'profile'
toggleEmail = None
success = None
@app.route('/change_success', methods = ['GET', 'POST'])
def change_success():
    global success
    print(success)
    data = request.json
    new_success = data.get('new_success')
    print(new_success)
    if new_success == "None":
        success = None
        print(success)
        return jsonify(success)
    return jsonify("eat dog"), 400


@app.template_filter('split_camel_case')
def split_camel_case(value):
    return ' '.join(re.findall(r'[A-Z][^A-Z]*', value))
app.jinja_env.filters['split_camel_case'] = split_camel_case
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    try:
        with shelve.open('admin') as adminDB:
            admin = adminDB[session.get('current_user')]
        isAdmin = True
    except:
        isAdmin = False
    global current_tab
    print(current_tab)
    current_user = None
    cart = None
    codes = None
    cooldown = None
    addresses = None
    users_orders = []
    with shelve.open('Orders') as ordersDB:
        for i in ordersDB:
            if ordersDB[i].user == session.get('current_user'):
                users_orders.append(copy.deepcopy(ordersDB[i]))
    users_orders.sort(key=lambda order: order.datetime, reverse=True)
    try:
        current_user = CurrentUser.fromEmail(session.get('current_user'))
        cart = current_user.Cart
        codes = current_user.Codes
        totalCodes = sum(codes.values())
        cooldown = current_user.Cooldown
        addresses = current_user.Addresses
        print(codes)
    except:
        current_user = None
    otpform = Otp()
    signoutform  = signOut()
    change_email = changeEmail()
    change_emailEmail = None
    change_password = changePassword()
    delete_account = deleteAccount()
    add_address = addAddress()
    global success
    global toggleEmail
    print(success)
    if request.method == 'POST' :
        if 'signout_submit' in request.form and signoutform.validate_on_submit():
            current_user = None
            session.pop('current_user')
            return redirect(url_for('about_us'))
        elif 'signout_cancel_submit' in request.form and signoutform.validate_on_submit():

            return redirect(url_for('profile'))
        elif 'change_email_submit' in request.form and change_email.validate_on_submit():
            change_emailEmail = change_email.email.data
            session['change_email'] = change_emailEmail
            print(change_email.email.data)
            otp = generateOTP.__call__(change_emailEmail)
            session['otp'] = otp
            print(session['otp'])
            toggleEmail = True
            success = "Please check your new email for the 6 digit code we just sent."

        elif 'otp_submit' in request.form and otpform.validate_on_submit():
            with shelve.open('users') as usersDB:
                temp = copy.deepcopy(usersDB[session.get('current_user')])
                temp.setEmail(session.get('change_email'))
                usersDB[temp.getEmail()] = temp
                del usersDB[session.get('current_user')]
            session['current_user'] = temp.getEmail()
            current_user = temp
            session.pop('change_email')
            toggleEmail = False
            success = "Email changed successfully"
            return redirect(url_for('profile'))

        elif 'change_password_submit' in request.form and change_password.validate_on_submit():
            with shelve.open('users') as usersDB:
                temp = copy.deepcopy(usersDB[session.get('current_user')])
                temp.setPassword(change_password.newPassword.data)
                usersDB[temp.getEmail()] = temp
            success = "Password changed successfully"
            return redirect(url_for('profile'))

        elif 'delete_submit' in request.form and delete_account.validate_on_submit():
            with shelve.open('users') as usersDB:
                del usersDB[session.get('current_user')]
            current_user = None
            session.pop('current_user')
            return redirect(url_for('about_us'))
        elif 'delete_cancel_submit' in request.form:
            return redirect(url_for('profile'))
        elif 'add_address_submit' in request.form and add_address.validate_on_submit():

            address = ', '.join(
                filter(None, [
                    add_address.zip.data,
                    add_address.street.data.title(),
                    add_address.buildingName.data.title() if add_address.buildingName.data else None,
                    str(add_address.blockNumber.data) if add_address.blockNumber.data else None,
                    add_address.unitNumber.data
                ])
            )
            current_user.addAddress(address)
            success = "Address added successfully"
            return redirect(url_for('profile'))
        else:
            print("Form validation failed:", otpform.errors, change_email.errors)
    if current_user is None:
        return redirect(url_for('sign_in'))
    return render_template('profile.html', active_page='profile',signoutform = signoutform, current_tab = current_tab,
                           current_user=current_user,  otpform=otpform, change_email = change_email,
                           change_emailEmail = change_emailEmail, change_password = change_password, cart = cart, codes = codes,
                           cooldown = cooldown, delete_account = delete_account, toggleEmail = toggleEmail, success = success, add_address = add_address, addresses = addresses, orders = users_orders, totalCodes= totalCodes
                           ,isAdmin = isAdmin)

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
@app.route('/remove_address/<int:addresss>', methods = ['GET', 'POST'])
def remove_address(addresss):
    global success
    with shelve.open('users') as usersDB:
        current_user = CurrentUser.fromEmail(session.get('current_user'))
    current_user.removeAddress(addresss)
    success = "Address removed successfully"
    return redirect(url_for('profile'))
@app.route('/updateadminaction', methods = ['POST'])
def updateadmin_action():
    global action
    action = request.json
    new_action = action.get('new_action')
    if new_action:
        action = new_action
        return jsonify(action)
    return jsonify("piss off"), 400

sort_orders = "date_latest"
@app.route('/update_orders_sort', methods = ['POST'])
def update_orders_sort():
    global sort_orders
    sort = request.json
    new_sort = sort.get('new_action')
    if new_sort:
        sort_orders = new_sort
        print(sort_orders)
        return jsonify(new_sort)
    return jsonify("piss off"), 400

def parse_order(s):
    pattern = re.compile(
        r'^(?=.*user_(?P<user>[^\s@]+@[^\s@]+\.[^\s@]+)(?=_))?(?=.*order_id_(?P<order_id>\d+))?(?=.*ref_num_(?P<ref_num>PN\d{8}))?.*date_(?P<state>latest|earliest)$'
    )
    match = pattern.match(s)
    if match:
        return {
            'state': f"date_{match.group('state')}",
            'user': match.group('user'),
            'orderId': match.group('order_id'),
            'refNum': match.group('ref_num')
        }
    return None


@app.route('/change_order_status/<order_id>/<new_status>', methods = ['GET','POST'])
def change_order_status(order_id, new_status):
    Order.updateStatus(order_id, new_status)
    return redirect(url_for('Admin'))


@app.route('/admin/download_orders', methods = ['GET', 'POST'])
def download_orders():
    from BizStats import exportXL
    return exportXL()
@app.route('/addAdmin/<user>', methods = ['GET', 'POST'])
def add_admin(user):
    try:
        with shelve.open('admin') as adminDB:
            admin = adminDB[session.get('current_user')]
        with shelve.open('users') as usersDB:
            print(usersDB[user].isAdmin())
            usersDB[user].addAdmin()
            print(usersDB[user].isAdmin()) #debug
        return redirect(url_for('Admin'))
    except:
        return redirect(url_for('about_us'))

@app.route('/removeAdmin/<user>', methods = ['GET', 'POST'])
def remove_admin(user):
    try:
        with shelve.open('admin') as adminDB:
            admin = adminDB[session.get('current_user')]
        with shelve.open('users') as usersDB:
            print(usersDB[user].isAdmin())
            usersDB[user].removeAdmin()
            print(usersDB[user].isAdmin()) #debug
        return redirect(url_for('Admin'))
    except:
        return redirect(url_for('about_us'))
@app.route('/admin', methods=['GET', 'POST'])
def Admin():
    from BizStats import GetStats
    try:

        with shelve.open('admin') as adminDB:
            admin = adminDB[session.get('current_user')]
            all_admins = {key: adminDB[key] for key in adminDB}

            for i in adminDB:
                print(i)
        with shelve.open('users') as usersDB:
            all_users = {key: usersDB[key] for key in usersDB}
            current_user = usersDB[session.get('current_user')]
        with shelve.open('tickets') as ticketDB:
            all_tickets = {key: ticketDB[key] for key in ticketDB}
    except:
        return redirect(url_for('about_us'))
    reply_ticket = replyTicket()
    stats = GetStats()
    print(stats)
    add_product = addProduct()
    modify_product = modifyProduct()
    global sort_orders
    orders = []
    print(f"i got hoes {sort_orders}")
    sort_conditions = parse_order(sort_orders)
    print(f"i got no hoes{sort_conditions}")
    v = 0
    if sort_conditions['state'] == 'date_latest':
        with shelve.open('Orders') as ordersDB:
            if sort_conditions['user']:
                v+=1
                for i in ordersDB:
                    first_u = sort_conditions['user'].index('_')
                    print(ordersDB[i].user, sort_conditions['user'][:first_u])
                    if ordersDB[i].user == sort_conditions['user'][:first_u]:
                        orders.append(copy.deepcopy(ordersDB[i]))
                for i in orders:
                    print(i)
            if sort_conditions['orderId']:
                if v == 0:
                    v += 1
                    for i in ordersDB:
                        print(ordersDB[i].id, sort_conditions['orderId'])
                        if str(ordersDB[i].id) == str(sort_conditions['orderId']):
                            orders.append(copy.deepcopy(ordersDB[i]))
                else:
                    for x in orders[:]:
                        print(x.id)

                        if str(x.id) != str(sort_conditions['orderId']):
                            orders.remove(x)
            if sort_conditions['refNum']:
                if v == 0:
                    v += 1
                    for i in ordersDB:
                        print(ordersDB[i].payment_method, sort_conditions['refNum'])
                        if ordersDB[i].payment_method == sort_conditions['refNum']:
                            orders.append(copy.deepcopy(ordersDB[i]))
                else:
                    print(orders)
                    for z in orders[:]:
                        print(z.payment_method, sort_conditions['refNum'])
                        if z.payment_method != sort_conditions['refNum']:
                            orders.remove(z)
            if v == 0:
                for i in ordersDB:
                    orders.append(copy.deepcopy(ordersDB[i]))
        orders.sort(key=lambda order: order.datetime, reverse=True)

    elif sort_conditions['state'] == 'date_earliest':
        with shelve.open('Orders') as ordersDB:
            if sort_conditions['user']:
                v += 1
                for i in ordersDB:

                    first_u = sort_conditions['user'].index('_')
                    print(ordersDB[i].user, sort_conditions['user'][:first_u])
                    if ordersDB[i].user == sort_conditions['user'][:first_u]:
                        orders.append(copy.deepcopy(ordersDB[i]))
            if sort_conditions['orderId']:
                if v == 0:
                    v += 1
                    for i in ordersDB:
                        print(ordersDB[i].id, sort_conditions['orderId'])
                        if str(ordersDB[i].id) == str(sort_conditions['orderId']):
                            orders.append(copy.deepcopy(ordersDB[i]))
                else:
                    for i in orders[:]:

                        if str(i.id) != str(sort_conditions['orderId']):
                            orders.remove(i)
            if sort_conditions['refNum']:
                if v == 0:
                    v += 1
                    for i in ordersDB:
                        print(ordersDB[i].payment_method, sort_conditions['refNum'])
                        if ordersDB[i].payment_method == sort_conditions['refNum']:
                            orders.append(copy.deepcopy(ordersDB[i]))
                else:
                    print(orders)
                    for z in orders[:]:
                        print(z.payment_method, sort_conditions['refNum'])
                        if z.payment_method != sort_conditions['refNum']:
                            orders.remove(z)
            if v == 0:
                for i in ordersDB:
                    orders.append(copy.deepcopy(ordersDB[i]))
        orders.sort(key=lambda order: order.datetime, reverse=False)
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
    return render_template('admin.html', add_product = add_product, action=action , modify_product = modify_product, orders = orders, stats = stats, all_users = all_users, all_admins = all_admins, current_user = current_user, tickets = all_tickets
                           ,reply_ticket= reply_ticket)

def getSimiliarProducts(product):

    weights = {}
    with shelve.open('products') as productsDB:
        categories = set(product.categories)
        keys = list(productsDB.keys())
        keys.pop(keys.index(product.id))

        for i in productsDB:
            if product.id != i and productsDB[i].quantity > 0:
                p_cat = set(productsDB[i].categories)
                weight = len(p_cat & categories) / len(p_cat | categories)   #jaccard similiarity
                weights[i] = weight

        total_weight = sum(weights.values())
        if total_weight == 0:  #avoid zero probabilities
            weights = {key: 1 for key in weights}
            total_weight = sum(weights.values())
        selected_object = random.choices(list(keys), weights=list(weights.values()), k = 8)
    return selected_object


@app.route('/catalog/product/<int:product_id>', methods = ['GET', 'POST'])
def product_detail(product_id):
    with shelve.open('products') as productsDB:
        product = productsDB[str(product_id)]
        all_products = {key: productsDB[key] for key in productsDB}

        if not product:
            return "Product not found",404
        similiar = getSimiliarProducts(product)
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
                           current_user=current_user, cart = cart, similiar = similiar, all_products = all_products)



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

    except:
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
    try:
        with shelve.open('users') as usersDB:
            current_user = usersDB[session.get('current_user')]
            current_user.addToCart(product_id)
            for i in current_user.Cart:
                with shelve.open('products') as productsDB:
                    print(f'{productsDB[str(i)]},,,, quantity: {current_user.Cart[i]}')
        return redirect(url_for('cart'))
    except:
        return redirect(url_for('sign_in'))
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
            Addresses = current_user.Addresses
        cart = current_user.Cart

        subtotal = 0
        for i in cart:
            if all_products[str(i)].quantity > cart.get(i):
                subtotal += all_products[str(i)].price * cart.get(i)
            else:
                print("out of stock")
        subtotal += 5
        global voucherUsed
        global discount
        global gifts
        global freeShipping
        global selected_address
        if discount:
            subtotal -= round((subtotal*(discount/100)),2)
        if freeShipping:
            subtotal -= 5

        global codeUsed

        return render_template('cart.html',active_page='cart', products=all_products, cart = cart, subtotal = subtotal, codes = codes, voucherUsed = voucherUsed
                               , discount = discount, gifts = gifts, freeShipping = freeShipping, codeUsed = codeUsed, current_user = current_user, addresses = Addresses, selected_address = selected_address)

    except Exception as e:
        print(e)
        return redirect(url_for('sign_in'))

selected_address = None

@app.route('/update-address', methods=['POST'])
def update_address():
    global selected_address
    data = request.get_json()
    selected_address = data.get('address')
    return jsonify({"message": "Address updated successfully", "selected_address": selected_address})
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
            usersDB[session.get('current_user')].updateCooldown(90)
            print(usersDB[session.get('current_user')].Codes[code])
    except KeyError as e:
          return jsonify({'error': 'Database error', 'details': str(e)}), 500

    print(code)

    return jsonify({'success': True, 'message': 'Code redeemed successfully'})

payment_session = {}
@app.route('/cart/checkout/<subtotal>/<address>', methods = ['GET', 'POST'])
def checkOut(subtotal,address):




        voucher = codeUsed
        print(voucher)

        with shelve.open('users') as usersDB:
            current_user = usersDB[session.get('current_user')]
            cart = current_user.Cart
            newOrder = Order(subtotal, cart, voucher, session.get('current_user'), address)
        id = newOrder.id
        payment_session[session.get('current_user')] = 600

        payment_thread = threading.Thread(target=updatePaymentSession, args=(session.get('current_user'),str(id)), daemon=True)
        payment_thread.start()
        return redirect(url_for('payment', orderid=id))

def updatePaymentSession(user_id, orderid):
    try:
        while payment_session.get(user_id, 0) > 0:
            payment_session[user_id] -= 1
            print(payment_session[user_id])
            time.sleep(1)
        payment_session.pop(user_id, None)
        if payment_session[user_id] == 0:
            Order.cancel_order(orderid)
    except Exception as e:
        print(f"Error in payment session thread: {e}")

@app.route('/payment/<orderid>' , methods = ['GET', 'POST'])
def payment(orderid):
    try:
        if payment_session[session.get('current_user')] > 0:
            with shelve.open('Orders') as orders:
                order = orders[str(orderid)]
                order_clone = copy.deepcopy(order)
                if order.user == session.get('current_user'):
                    qr = generatePayNowQR.generatePayNowQR(str(orders[str(orderid)].subtotal), random.randint(10000000, 99999999))
                    img_64 = base64.b64encode(qr[0].read()).decode('utf-8')
                    return render_template('payment.html', order = order_clone, img_64=img_64, ref = qr[1], session = payment_session[session.get('current_user')])
                else:
                    return redirect(url_for('cart'))
        else:

            return redirect(url_for('cart'))
    except:

        return redirect(url_for('cart'))


@app.route('/payment/cancel_order/<orderid>', methods = ['GET', 'POST'])
def cancel_order(orderid):
    if Order.getUser(orderid) == session.get('current_user') and Order.getStatus(orderid) == "PaymentPending":
        Order.cancel_order(str(orderid))
        payment_session.pop(session.get('current_user'))
        return redirect(url_for('cart'))
    else:
        return redirect(url_for('cart'))


@app.route('/payment/confirmorder/<orderid>/<ref>', methods = ['GET', 'POST'])
def confirm_order(orderid, ref):
    if Order.getUser(orderid) == session.get('current_user') and Order.getStatus(orderid) == "PaymentPending":
        global codeUsed
        global voucherUsed
        global discount
        global gifts
        global freeShipping
        global success
        global current_tab

        voucherUsed = False
        codeUsed = None
        discount = None
        gifts = None
        freeShipping = False
        current_tab = "order_history"
        success = "Order successfully placed!"
        payment_session.pop(session.get('current_user'))
        with shelve.open('users') as usersDB:
            current_user = usersDB[session.get('current_user')]
            current_user.clearCart()
        Order.updateStatus(orderid, "PaymentProcessing")
        Order.update_payment_method(orderid, f'PN{ref}')
        return redirect(url_for('profile'))
    else:
        print('something went wrong')
        Order.cancel_order(orderid)
        return redirect(url_for('cart'))



@app.route('/support', methods=['GET', 'POST'])
def support():
    try:
        with shelve.open('users') as usersDB:
            current_user = usersDB[session.get('current_user')]
    except:
        return redirect(url_for('sign_in'))

    open_ticket = openTicket()
    if request.method == 'POST':
        if 'open_ticket_submit' in request.form and open_ticket.validate_on_submit():
            print(Ticket(current_user.getEmail(), open_ticket.issue.data, open_ticket.body.data))
            open_ticket.body.data = ""
            open_ticket.issue.data = ""
            global success
            success = "Ticket successfully submitted!"
            return redirect(url_for('profile'))

    return render_template('support.html', open_ticket=open_ticket, current_user=current_user, active_page = "profile")

@app.route('/reply_ticket/<id>', methods=['GET', 'POST'])
def reply_ticket(id):
    try:
        with shelve.open('admin') as adminDB:
            admin = adminDB[session.get('current_user')]
    except:
        return redirect(url_for('about_us'))
    open_ticket = openTicket()
    with shelve.open("tickets") as tickets:
        ticket = tickets[str(id)]
        ticket.add_reply(session.get('current_user'), open_ticket.body.data)
    return redirect(url_for('Admin'))

@app.route('/close_ticket/<id>', methods=['GET', 'POST'])
def close_ticket(id):
    try:
        with shelve.open('admin') as adminDB:
            admin = adminDB[session.get('current_user')]
    except:
        return redirect(url_for('about_us'))

    with shelve.open("tickets") as tickets:
        ticket = tickets[str(id)]
        ticket.change_status("Closed")
    return redirect(url_for('Admin'))
@app.route('/open_ticket/<id>', methods=['GET', 'POST'])
def open_ticket(id):
    try:
        with shelve.open('admin') as adminDB:
            admin = adminDB[session.get('current_user')]
    except:
        return redirect(url_for('about_us'))

    with shelve.open("tickets") as tickets:
        ticket = tickets[str(id)]
        ticket.change_status("Open")
    return redirect(url_for('Admin'))
