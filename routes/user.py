from flask import render_template, render_template_string, request, url_for, redirect, session, Blueprint
import thisclass.Myclass as pnt
import os
from dotenv import load_dotenv

user_bp = Blueprint('main', __name__)

load_dotenv()
DATABASE = os.getenv("DATABASE_URL")
cart = pnt.Cart()
menus = pnt.EachData()


@user_bp.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@user_bp.route('/completed', methods=['POST', 'GET'])
def completed():
    baranggay, municipality, province, name, phoneNo = request.form.get('brgy'), request.form.get('municipality'), request.form.get('province'), request.form.get('name'), request.form.get('phone')
    

    isGcash = session.get('isGcash')
    this_cart = []
    if isGcash == 0:
        
        total_price = int(cart.getTotal() + 20)
        money = session.get('money_from_cus')
        change = money-total_price
        for i in cart.showList():
            for j in i:
                this_cart.append(j)
        session.clear()
        
        return render_template('completed.html', this_cart=this_cart, total_price=total_price, change=change, money=money)
    this_cart = []
    total_price = int(cart.getTotal() + 20)
    money = "PAID WITHIN GCASH"
    change = "PAID WITHIN GCASH"
    for i in cart.showList():
        for j in i:
            this_cart.append(j)
    session.clear()
    return render_template('completed.html', this_cart=this_cart, total_price=total_price, change=change, money=money)

@user_bp.route('/processPayment', methods=['POST', 'GET'])
def processPayment():
    input_field = request.form.get('processingField')
    isGcash = session.get('isGcash')
    if pnt.checkIfInt(input_field):
        if isGcash==1:
            reference = str(input_field)
            if len(reference)!=13:
                return "incorrect reference number"
            
            divString = "<h1>THANK YOU FOR CHOOSING US!</h1>"
            return render_template('processed.html', divString=divString)
        elif isGcash==0:
            total_price = cart.getTotal() + 20 # plus 20 for delivery fee
            money = int(input_field)
            session['money_from_cus'] = money
            change = 0
            if money<total_price:
                short=total_price-money
                divString = f"<h2>You are ${ short } short. Please pay equal or higher than to total amount</h2>"
                return render_template('processed.html', money=money, total_price=total_price, divString=divString)
                
            elif money==total_price:
                divString = "<h1>THANK YOU FOR CHOOSING US!</h1>"
                
                return render_template('processed.html', divString=divString)

            
            change = money-total_price
            divString = f"""<h1>THANK YOU FOR CHOOSING US</h1>
                            <h5>Your Change is ${ change }</h5>
                            <h5>Expect this amount from the rider</h5>
                        """
            return render_template('processed.html',divString=divString)
    
    return f"please enter a form of number, you entered: {input_field}"

@user_bp.route('/formOfPayment', methods=['POST', 'GET'])
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

@user_bp.route('/toCheckout', methods=['POST', 'GET'])
def toCheckout():
    total_amount = cart.getTotal()
    plusDf = total_amount+20
    formString = session.get('formString', "")
    print(formString)
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

@user_bp.route('/userPage', methods=['POST', 'GET'])
def userPage():
    return render_template("user-page.html") 

@user_bp.route('/option', methods=['POST', 'GET'])
def user():
    if request.method == 'POST':
        if request.form.get('user'):
            return "user"
        elif request.form.get('admin'):
            return "admin"
    elif request.method == 'GET':
        return "get"
    return "something wrong"