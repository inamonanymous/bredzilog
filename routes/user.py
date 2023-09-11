from flask import render_template, render_template_string, request, url_for, redirect, session, Blueprint, make_response
import thisclass.Myclass as pnt
import os
from dotenv import load_dotenv

user_bp = Blueprint('main', __name__)

load_dotenv()
DATABASE = os.getenv("DATABASE_URL")
cart = pnt.Cart()
menus = pnt.EachData()
#g_user_data = pnt.UserData()

@user_bp.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@user_bp.route('/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect(url_for('main.userPage'))
    

@user_bp.route('/completed', methods=['POST', 'GET'])
def completed():
    if 'isGcash' and 'money_from_cus' and 'nameuser' in session:
        baranggay,street, houseNo , municipality, province, name, phoneNo = request.form.get('brgy'), request.form.get('street'), request.form.get('houseNo'), request.form.get('municipality'), request.form.get('province'), request.form.get('name'), request.form.get('phone')
        address = f"Brgy: {baranggay}, Street: {street}, House Number: {houseNo}, Municipality: {municipality}, Province: {province}"
        isGcash = session.get('isGcash')
        receipt_data = pnt.ReceiptsData()
        if isGcash == 0:
            
            money = session.get('money_from_cus')
            total_price = int(cart.getTotal() + 20)
            change = money-total_price
            unique = pnt.ReceiptsData.generate_unique_id()
            
            if cart.showList:
                receipt = pnt.Receipts(int(), str(unique), str(name), str(address), str(phoneNo), int(money), str(), int(total_price), cart.showList)
                receipt_data.save_to_db(receipt)
                menus.decrement_qty(receipt)
                
                clear_browser_session()
                return render_template('completed.html', this_cart=cart.showList, total_price=total_price, change=change, money=money)
        
            return redirect(url_for('main.deliverSetup'))
        total_price = int(cart.getTotal() + 20)
        money = "PAID WITHIN GCASH"
        change = "PAID WITHIN GCASH"
        referenceNo = session.get('referenceNo')
        unique = pnt.ReceiptsData.generate_unique_id()
        if cart.showList:
            receipt = pnt.Receipts(int(), unique, name, address, phoneNo, int(), referenceNo, total_price, cart.showList)
            menus.decrement_qty(receipt)
            receipt_data.save_to_db(receipt)
            
            clear_browser_session()
            return render_template('completed.html', this_cart=cart.showList, total_price=total_price, change=change, money=money)
        return redirect(url_for('main.deliverSetup'))
    return redirect(url_for('main.userPage'))

@user_bp.route('/processPayment', methods=['POST', 'GET'])
def processPayment():
    g_user_data = pnt.UserData()
    if 'user-email' or 'nameuser' in session:
        g_user_data = pnt.UserData()
        user_login = g_user_data.getByEmail(str(session.get('user-email')))
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
                return render_template('processed.html', divString=divString, nameuser=nameuser, user_login=user_login, myBool=True)
            elif isGcash==0:
                total_price = cart.getTotal() + 20 # plus 20 for delivery fee
                money = int(input_field)
                session['money_from_cus'] = money
                change = 0
                if money<total_price:
                    short=total_price-money
                    return render_template('processed.html', money=money, total_price=total_price, nameuser=nameuser, myBool=False, short=short, user_login=user_login)
                    
                elif money==total_price:
                    divString = "<h1>THANK YOU FOR CHOOSING US!</h1>"
                    
                    return render_template('processed.html', divString=divString, nameuser=nameuser, myBool=True, user_login=user_login)

                
                change = money-total_price
                divString = f"""<h1>THANK YOU FOR CHOOSING US</h1>
                                <h5>Your Change is ₱{ change }</h5>
                                <h5>Expect this amount from the rider</h5>
                            """
                return render_template('processed.html',divString=divString, nameuser=nameuser, myBool=True, user_login=user_login)
    
    return f"please enter a form of number, you entered: {input_field}"

@user_bp.route('/formOfPayment', methods=['POST', 'GET'])
def formOfPayment():
    formString = str()
    if session.get('isDineIn'):
        if 'g-cash' in request.form:
            session["isGcash"] = 1
            formString = """
                            <img src="../static/img/g-cash.jpg" alt="Admin's G-Cash QR" width="230" height="225"><form action="/processPayment" method="post" style="margin-top: 10px"><!-- G-Cash form fields --><input type="number" name="processingField" placeholder="Enter Reference Number" class="form-control" style="max-width: 200px" required><input type="submit" value="Submit G-Cash" name="fromGcash" class="font-monospace btn btn-outline-primary btn-rounded btn-md mt-3"></form>
                        """
            print(session.get('isDineIn'))

        if 'cash-on-arr' in request.form:
            session["isGcash"] = 0
            formString = """
                        <form action="/processPayment" method="post"><!-- Cash-on-Arrival form fields --><input type="submit" value="Submit Cash" name="fromCash" class="font-monospace btn btn-outline-success btn-rounded btn-md mt-3"></form>
                     """

        if formString:
            session['formString'] = formString
            
    
    if 'cash-on-del' in request.form:
        session["isGcash"] = 0
        formString = """
                        <form action="/processPayment" method="post"><!-- Cash-on-Delivery form fields --><input type="number" name="processingField" placeholder="Enter cash amount" class="form-control" style="max-width: 200px" required><input type="submit" value="Submit Cash" name="fromCash" class="font-monospace btn btn-outline-success btn-rounded btn-md mt-3"></form>
                     """
    elif 'g-cash' in request.form:
        session["isGcash"] = 1
        formString = """
                        <img src="../static/img/g-cash.jpg" alt="Admin's G-Cash QR" width="230" height="225"><form action="/processPayment" method="post" style="margin-top: 10px"><!-- G-Cash form fields --><input type="number" name="processingField" placeholder="Enter Reference Number" class="form-control" style="max-width: 200px" required><input type="submit" value="Submit G-Cash" name="fromGcash" class="font-monospace btn btn-outline-primary btn-rounded btn-md mt-3"></form>
                     """
    if formString:
        session['formString'] = formString
        
    return redirect(url_for('main.toCheckout'))

@user_bp.route('/toCheckout', methods=['POST', 'GET'])
def toCheckout():
    total_amount = cart.getTotal()
    plusDf = total_amount+20
    formString = session.get('formString', "")
    if session.get('isDineIn'):
        if total_amount==0:
            return redirect(url_for('main.tableReservation'))
        return render_template('to-checkout.html', total_amount=total_amount, formString=formString, plusDf=plusDf, isDineIn=session.get('isDineIn'))

    if total_amount==0:
        return redirect(url_for('main.deliverSetup'))
    
    return render_template('to-checkout.html', total_amount=total_amount, formString=formString, plusDf=plusDf, isDineIn=session.get('isDineIn'))

@user_bp.route('/tableReservation', methods=['POST', 'GET'])
def tableReservation():
    if session.get('nameuser') or session.get('user-email') is not None:
        session['isDineIn'] = True
        total = cart.getTotal()
        return render_template('table-reservation.html', menu=menus, original_values=cart.showList[::-1], total=total)
    return redirect(url_for('main.userPage'))

@user_bp.route('/deliverSetup', methods=['POST', 'GET'])
def deliverSetup():
    if session.get('nameuser') or session.get('user-email') is not None:
        session['isDineIn'] = False
        total = cart.getTotal()
        return render_template('deliver-setup.html', menu=menus, original_values=cart.showList[::-1], total=total)
    return redirect(url_for('main.userPage'))

@user_bp.route('/deleteItem/<int:item_id>', methods=["POST", "GET"])
def deleteItem(item_id):
    if 'user-email' or 'nameuser' in session:
        if not session.get('isDineIn'):
            cart.deleteItem(item_id)
            return redirect(url_for('main.deliverSetup'))
        cart.deleteItem(item_id)
        return redirect(url_for('main.tableReservation'))
    return redirect(url_for('main.userPage'))

@user_bp.route('/addCart/<int:item_id>', methods=["POST", "GET"])
def addCart(item_id):
    if 'user-email' or 'nameuser' in session:
        if not session.get('isDineIn'):
            cart.addItem(item_id)
            return redirect(url_for('main.deliverSetup'))
        cart.addItem(item_id)
        return redirect(url_for('main.tableReservation'))
    return redirect(url_for('main.userPage'))

@user_bp.route('/signedUp', methods=['POST', 'GET'])
def signedUp():
    g_user_data = pnt.UserData()
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
    g_user_data = pnt.UserData()
    name, surname, phone, brgy, street, houseNo, municipality, province = request.form.get('name'), request.form.get('surname'), request.form.get('phone'), request.form.get('brgy'), request.form.get('street'), request.form.get('houseNo'), request.form.get('municipality'), request.form.get('province')
    if request.method == "POST":
        user_login = g_user_data.getByEmail(str(session.get('user-email', "")))
        if user_login is not None and 'user-email' in session:
            user_login.set_contact(name, surname, phone)
            user_login.set_address(brgy, street, houseNo, municipality, province)
            print(user_login)
            print(str(user_login.get_address))
            g_user_data.updateContact(user_login)
            g_user_data.saveAddress(user_login)
            
            return redirect(url_for('main.userDashboard'))
        
        return redirect(url_for('main.userSettings'))
    
    return redirect(url_for('main.userSettings'))

@user_bp.route('/userSettings', methods=['POST', 'GET'])
def userSettings():
    g_user_data = pnt.UserData()
    user_login = g_user_data.getByEmail(str(session.get('user-email', "")))
    if user_login is not None and 'user-email' in session:
        brgy, houseNo, street, municipality, province = user_login.get_per_address
        return render_template('user-settings.html', user_login=user_login, brgy=brgy, houseNo=houseNo, street=street, municipality=municipality, province=province)
    return redirect(url_for('main.userPage'))



@user_bp.route('/userDashboard', methods=['POST', 'GET'])
def userDashboard():
    g_user_data = pnt.UserData()
    if 'user-email' in session:
        user_login = g_user_data.getByEmail(str(session.get('user-email', "")))
        cart.clearItems()
        return render_template('user-dashboard.html', nameuser=session.get('nameuser', ""), user_login=user_login, email=user_login.get_email)
    elif 'nameuser' in session:
        cart.clearItems()
        return render_template('user-dashboard.html', nameuser=session.get('nameuser', ""))    
    return redirect(url_for('main.userPage'))
    
@user_bp.route('/signedin', methods=['POST', 'GET'])
def signedin():
    g_user_data = pnt.UserData()
    email, password = request.form.get('user-email'), request.form.get('user-password')
    if request.method == "POST":
        if g_user_data.loginIsTrue(email, password):
            g_user_login = g_user_data.getByEmail(email)
            if g_user_login is None:
                session.clear()
                return "session expired"
            session['user-email'] = email
            session['nameuser'] = f"{g_user_login.get_firstname}, {g_user_login.get_surname}"
            return redirect(url_for('main.userDashboard'))
        else:
            return f"invalid username or password"
    return redirect(url_for('main.userPage'))

@user_bp.route('/userPage', methods=['POST', 'GET'])
def userPage():
    session.clear()
    if request.form.get('signIn'):
        return render_template('user-signin.html')
    user_option_str = """
                        <form action="/userPage" method="post"> <input type="text" name="nameuser" id="nameuser" class="form-control" style="width: 30%;"><br><button class="btn btn-outline-success mt-2" type="submit">Enter</button></form>
                      """
    nameuser = request.form.get('nameuser')
    if nameuser is not None:
        if len(nameuser) > 1:
            
            session['nameuser'] = nameuser
            
            return redirect(url_for('main.userDashboard'))
        return "Enter valid name" 
    return render_template("user-page.html", user_option_str=user_option_str)


def clear_browser_session():
    session.pop('isGcash', None)
    session.pop('money_from_cus', None)

