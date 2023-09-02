from flask import render_template, render_template_string, request, url_for, redirect, session, Blueprint, make_response
import thisclass.Myclass as pnt
import os
from dotenv import load_dotenv

user_bp = Blueprint('main', __name__)

load_dotenv()
DATABASE = os.getenv("DATABASE_URL")
cart = pnt.Cart()
menus = pnt.EachData()
g_user_data = pnt.UserData()

@user_bp.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@user_bp.route('/completed', methods=['POST', 'GET'])
def completed():
    baranggay,street, houseNo , municipality, province, name, phoneNo = request.form.get('brgy'), request.form.get('street'), request.form.get('houseNo'), request.form.get('municipality'), request.form.get('province'), request.form.get('name'), request.form.get('phone')
    address = f"Brgy: {baranggay}, Street: {street}, House Number: {houseNo}, Municipality: {municipality}, Province: {province}"
    isGcash = session.get('isGcash')
    this_cart = []
    receipt_data = pnt.ReceiptsData()
    if isGcash == 0:
        money = session.get('money_from_cus')
        total_price = int(cart.getTotal() + 20)
        change = money-total_price
        unique = pnt.ReceiptsData.generate_unique_id()
        receipt = pnt.Receipts(unique, name, address, phoneNo, money, str(), total_price)
        receipt_data.save_to_db(receipt)

        for i in cart.showList():
            for j in i:
                this_cart.append(j)
        clearAllSession()
        
        return render_template('completed.html', this_cart=this_cart, total_price=total_price, change=change, money=money)
    this_cart = []
    total_price = int(cart.getTotal() + 20)
    money = "PAID WITHIN GCASH"
    change = "PAID WITHIN GCASH"
    referenceNo = session.get('referenceNo')
    unique = pnt.ReceiptsData.generate_unique_id()
    receipt = pnt.Receipts(unique, name, address, phoneNo, int(), referenceNo, total_price)
    receipt_data.save_to_db(receipt)

    for i in cart.showList():
        for j in i:
            this_cart.append(j)
    clearAllSession()
    return render_template('completed.html', this_cart=this_cart, total_price=total_price, change=change, money=money)

@user_bp.route('/processPayment', methods=['POST', 'GET'])
def processPayment():
    input_field = request.form.get('processingField')
    isGcash = session.get('isGcash')
    nameuser = session.get('nameuser', "")
    if pnt.checkIfInt(input_field):
        if isGcash==1:
            reference = str(input_field)
            if len(reference)!=13:
                return "incorrect reference number"
            session['referenceNo'] = reference
            divString = "<h1>THANK YOU FOR CHOOSING US!</h1>"
            return render_template('processed.html', divString=divString, nameuser=nameuser)
        elif isGcash==0:
            total_price = cart.getTotal() + 20 # plus 20 for delivery fee
            money = int(input_field)
            session['money_from_cus'] = money
            change = 0
            if money<total_price:
                short=total_price-money
                divString = f"<h2>You are ${ short } short. Please pay equal or higher than to total amount</h2>"
                return render_template('processed.html', money=money, total_price=total_price, divString=divString, nameuser=nameuser)
                
            elif money==total_price:
                divString = "<h1>THANK YOU FOR CHOOSING US!</h1>"
                
                return render_template('processed.html', divString=divString, nameuser=nameuser)

            
            change = money-total_price
            divString = f"""<h1>THANK YOU FOR CHOOSING US</h1>
                            <h5>Your Change is ${ change }</h5>
                            <h5>Expect this amount from the rider</h5>
                        """
            return render_template('processed.html',divString=divString, nameuser=nameuser)
    
    return f"please enter a form of number, you entered: {input_field}"

@user_bp.route('/formOfPayment', methods=['POST', 'GET'])
def formOfPayment():
    formString = str()
    if 'cash-on-del' in request.form:
        session["isGcash"] = 0
        formString = """
                        <form action="/processPayment" method="post"><!-- Cash-on-Delivery form fields --><input type="number" name="processingField" placeholder="Enter cash amount" class="form-control" style="max-width: 200px" required><input type="submit" value="Submit Cash" name="fromCash" class="font-monospace btn btn-success btn-rounded btn-md mt-3"></form>
                     """
    elif 'g-cash' in request.form:
        session["isGcash"] = 1
        formString = """
                        <img src="../static/img/g-cash.jpg" alt="Admin's G-Cash QR" width="230" height="225"><form action="/processPayment" method="post" style="margin-top: 10px"><!-- G-Cash form fields --><input type="number" name="processingField" placeholder="Enter Reference Number" class="form-control" style="max-width: 200px" required><input type="submit" value="Submit G-Cash" name="fromGcash" class="font-monospace btn btn-primary btn-rounded btn-md mt-3"></form>
                     """
    if formString:
        session['formString'] = formString
        
    return redirect(url_for('main.toCheckout'))

@user_bp.route('/toCheckout', methods=['POST', 'GET'])
def toCheckout():
    total_amount = cart.getTotal()
    plusDf = total_amount+20
    formString = session.get('formString', "")
    if total_amount==0:
        return redirect(url_for('main.deliverSetup'))
    
    return render_template('to-checkout.html', total_amount=total_amount, formString=formString, plusDf=plusDf)

@user_bp.route('/deliverSetup', methods=['POST', 'GET'])
def deliverSetup():
    
    menu = menus.items
    my_cart = cart.showList()
    original_values = []
    for i in my_cart:
        for j in i:
            original_values.append(j)
    total = cart.getTotal()
    return render_template('deliver-setup.html', menu=menu, original_values=original_values, total=total), 200

@user_bp.route('/deleteItem/<int:item_id>', methods=["GET"])
def deleteItem(item_id):
    cart.deleteItem(item_id)
    return redirect(url_for('main.deliverSetup'))

@user_bp.route('/addCart', methods=["POST", "GET"])
def addCart():
    menu = menus.items
    btn_val = int(request.form.get('add-cart'))
    selected_product = None
    for i in menu:
        if i.id == btn_val:
            selected_product = i
            break
    if selected_product:
        cart.addItem(pnt.Item(selected_product.getId(), selected_product.getName(), selected_product.getPrice(), selected_product.getType()))
        print(f"{selected_product.name} added to cart.")
    else:
        print("Invalid product ID.")
    
    return redirect(url_for('main.deliverSetup'))

@user_bp.route('/signedUp', methods=['POST', 'GET'])
def signedUp():
    
    if request.method == 'POST':
        firstname = request.form.get('firstName')
        surname = request.form.get('surname')
        email = request.form.get('email')
        phone = request.form.get('number')
        password = request.form.get('password')
        password2 = request.form.get('confirmPassword')

        if g_user_data.checkIfExists(email):
            return "email already exists"
        elif password==password2:
            newUser = pnt.User(firstname, surname, email, phone, password)
            g_user_data.save(newUser)
            return render_template('user-signin.html')

        return render_template('sign-up-page.html')
        
    return render_template('sign-up-page.html')

@user_bp.route('/signUpPage', methods=['POST', 'GET'])
def signUpPage():
    return render_template('sign-up-page.html')

    


@user_bp.route('/updateSettings', methods=['POST', 'GET'])
def updateSettings():
    brgy, street, houseNo, municipality, province = request.form.get('brgy'), request.form.get('street'), request.form.get('houseNo'), request.form.get('municipality'), request.form.get('province')
    if request.method == "POST":
        user_login = g_user_data.getByEmail(str(session.get('user-email', "")))
        if user_login is not None and 'user-email' in session:
            user_login.set_address(brgy, street, houseNo, municipality, province)
            g_user_data.saveAddress(user_login)
            
            return redirect(url_for('main.userDashboard'))
        print(f"prob1{user_login}")
        print("prob1"+str(session.get('user-email', "")))
        return redirect(url_for('main.userSettings'))
    print(f"prob2{user_login}")
    print("prob2"+str(session.get('user-email', "")))
    return redirect(url_for('main.userSettings'))

@user_bp.route('/userSettings', methods=['POST', 'GET'])
def userSettings():
    user_login = g_user_data.getByEmail(str(session.get('user-email', "")))
    if user_login is not None and 'user-email' in session:
        return render_template('user-settings.html', user_login=user_login)
    return redirect(url_for('main.userPage'))

@user_bp.route('/userDashboard', methods=['POST', 'GET'])
def userDashboard():
    if 'user-email' in session:
        user_login = g_user_data.getByEmail(str(session.get('user-email', "")))
        return render_template('user-dashboard.html', nameuser=session.get('nameuser', ""), user_login=user_login, email=user_login.email)
    return render_template('user-dashboard.html', nameuser=session.get('nameuser', ""), user_login=user_login, email=user_login.email)

@user_bp.route('/signedin', methods=['POST', 'GET'])
def signedin():
    email, password = request.form.get('user-email'), request.form.get('user-password')
    
    if request.method == "POST":
        if g_user_data.loginIsTrue(email, password):
            g_user_login =  g_user_data.getByEmail(email)
            if g_user_login is None:
                session.pop('user-email', None)
                return "session expired"
            session['user-email'] = email
            session['nameuser'] = f"{g_user_login.firstname}, {g_user_login.surname}"
            return redirect(url_for('main.userDashboard'))
        else:
            return f"invalid username or password"
    return redirect(url_for('main.userPage'))

@user_bp.route('/userPage', methods=['POST', 'GET'])
def userPage():
    if request.form.get('signIn'):
        return render_template('user-signin.html')

    user_option_str = """
                        <form action="/userPage" method="post"> <input type="text" name="nameuser" id="nameuser"><button class="btn btn-danger mt-2" type="submit">Enter</button></form>
                      """
    nameuser = request.form.get('nameuser')
    if nameuser is not None:
        if len(nameuser) > 1:
            session['nameuser'] = nameuser
            user_option_str = f"""
                            <h3> Hello {nameuser}
                            <a href="/tableReservation">
                                        <button class="btn btn-danger mt-2" style="margin-left: 20px;" name="admin">Table Reservation</button>
                                    </a>
                                    <a href="/deliverSetup">
                                        <button class="btn btn-danger mt-2" style="margin-left: 20px;" name="admin">Deliver Food</button>
                                    </a>
                            """
            return render_template("user-page.html", user_option_str=user_option_str)
        return "Enter valid name" 
    return render_template("user-page.html", user_option_str=user_option_str)


def clearAllSession():
    session.pop('formString', None)
    session.pop('isGcash', None) 
    session.pop('money_from_cus', None)
    session.pop('nameuser', None)