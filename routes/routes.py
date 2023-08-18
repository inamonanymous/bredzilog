from flask import render_template, render_template_string, request, url_for, redirect, session, Blueprint
import thisclass.Myclass as pnt
import os

from dotenv import load_dotenv

rou_bp = Blueprint('main', __name__)

load_dotenv()
DATABASE = os.getenv("DATABASE_URL")
cart = pnt.Cart()
menus = pnt.EachData(DATABASE)


@rou_bp.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@rou_bp.route('/completed', methods=['POST', 'GET'])
def completed():
    this_cart = []
    for i in cart.showList():
        for j in i:
            this_cart.append(j)

    return render_template('completed.html', this_cart=this_cart)

@rou_bp.route('/processPayment', methods=['POST', 'GET'])
def processPayment():
    session['divString'] = str()
    input_field = request.form.get('processingField')
    isGcash = session.get('isGcash')
    if pnt.checkIfInt(input_field):
        if isGcash==1:
            reference = str(input_field)
            if len(reference)!=13:
                return "incorrect reference number"
            session.clear()
            divString = "<h1>THANK YOU FOR CHOOSING US!</h1>"
            return render_template('processed.html', divString=divString)
        elif isGcash==0:
            total_price = session.get('totalPrice') + 20 # plus 20 for delivery fee
            money = int(input_field)
            change = 0
            if money<total_price:
                short=total_price-money
                myString = f"<h2>You are ${ short } short. Please pay equal or higher than to total amount</h2>"
                session['divString'] = myString
                divString = session.get('divString', "")

                return render_template('processed.html', money=money, total_price=total_price, divString=divString)
                
            elif money==total_price:
                divString = "<h1>THANK YOU FOR CHOOSING US!</h1>"
                session.clear()
                return render_template('processed.html', divString=divString)

            session.clear()    
            change = money-total_price
            myString = f"""<h1>THANK YOU FOR CHOOSING US</h1>
                            <h5>Your Change is ${ change }</h5>
                            <h5>Expect this amount from the rider</h5>
                        """
            session['divString'] = myString
            divString = session.get('divString', "")
            return render_template('processed.html',divString=divString)
    
    return f"please enter a form of number, you entered: {input_field}"

@rou_bp.route('/formOfPayment', methods=['POST', 'GET'])
def formOfPayment():
    formString = str()
    if 'cash-on-del' in request.form:
        session["isGcash"] = 0
        formString = """
            <form action="/processPayment" method="post">
                <!-- Cash-on-Delivery form fields -->
                <input type="number" name="processingField" placeholder="Enter cash amount" class="form-control" style="max-width: 200px" required>
                <input type="submit" value="Submit Cash" name="fromCash" class="font-monospace btn btn-success btn-rounded btn-md mt-3">
            </form>
        """
    elif 'g-cash' in request.form:
        session["isGcash"] = 1
        formString = """
            <img src="../static/img/g-cash.jpg" alt="Girl in a jacket" width="230" height="225">
            <form action="/processPayment" method="post" style="margin-top: 10px">
                <!-- G-Cash form fields -->
                <input type="number" name="processingField" placeholder="Enter Reference Number" class="form-control" style="max-width: 200px" required>
                <input type="submit" value="Submit G-Cash" name="fromGcash" class="font-monospace btn btn-primary btn-rounded btn-md mt-3">
            </form>
        """
    if formString:
        session['formString'] = formString
        
    return redirect(url_for('main.toCheckout'))

@rou_bp.route('/toCheckout', methods=['POST', 'GET'])
def toCheckout():
    total_amount = session.get('totalPrice')
    plusDf = total_amount+20
    formString = session.get('formString', "")
    print(formString)
    if total_amount==0:
        return redirect(url_for('main.deliverSetup'))
    
    return render_template('to-checkout.html', total_amount=total_amount, formString=formString, plusDf=plusDf)

@rou_bp.route('/deliverSetup', methods=['POST', 'GET'])
def deliverSetup():
    menu = menus.items
    my_cart = cart.showList()
    original_values = []
    for i in my_cart:
        for j in i:
            original_values.append(j)
    session['totalPrice'] = cart.getTotal()
    total = session.get('totalPrice', "")
    return render_template('deliver-setup.html', menu=menu, original_values=original_values, total=total), 200

@rou_bp.route('/deleteItem/<int:item_id>', methods=["GET"])
def deleteItem(item_id):
    cart.deleteItem(item_id)
    return redirect(url_for('main.deliverSetup'))

@rou_bp.route('/addCart', methods=["POST", "GET"])
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

@rou_bp.route('/userPage', methods=['POST', 'GET'])
def userPage():
    return render_template("user-page.html") 

@rou_bp.route('/adminPage', methods=['POST', 'GET'])
def adminPage():
    return render_template("admin-page.html")

@rou_bp.route('/option', methods=['POST', 'GET'])
def user():
    if request.method == 'POST':
        if request.form.get('user'):
            return "user"
        elif request.form.get('admin'):
            return "admin"
    elif request.method == 'GET':
        return "get"
    return "something wrong"