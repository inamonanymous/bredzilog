from flask import Flask, render_template, request, url_for, g, redirect, session
import sqlite3
import thisclass.Myclass as pnt

app = Flask(__name__)
app.secret_key = "~$a3F@#718a4z"
DATABASE = 'bredzilog.db'
cart = pnt.Cart()
menus = pnt.EachData(DATABASE)


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        # Enable foreign key support for SQLite
        db.execute('PRAGMA foreign_keys = ON')
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/', methods=['POST', 'GET'])
def index():
    return render_template('index.html')

@app.route('/processPayment', methods=['POST', 'GET'])
def processPayment():
    isGcash = session.get('isGcash')
    change = 0
    if isGcash==1:
        return "gcash-mode"
    elif isGcash==0:
        input_field = request.form.get('cashField')
        isInt = pnt.checkIfInt(input_field)
        total_price = session.get('totalPrice') + 20
        if isInt:
            money = int(input_field)
            if money<total_price:
                return f"You can't pay lower than the total price, Sorry:) \n Amount Entered: {money} \n Expected Amount:{total_price} or {total_price}+"
            change = money-total_price
            return f"Your Change is: {change} \n Expect this amount from the Rider!"
        else:
            return f"please enter a form of number, you entered: {input_field}"

    return redirect(url_for('formOfPayment'))

@app.route('/formOfPayment', methods=['POST', 'GET'])
def formOfPayment():
    formString = str()
    if 'cash-on-del' in request.form:
        session["isGcash"] = 0
        formString = """
            <form action="/processPayment" method="post">
                <!-- Cash-on-Delivery form fields -->
                <input type="number" name="cashField" placeholder="Enter cash amount" class="form-control" style="max-width: 200px">
                <input type="submit" value="Submit Cash" name="fromCash" class="font-monospace btn btn-success btn-rounded btn-md mt-3">
            </form>
        """
    elif 'g-cash' in request.form:
        session["isGcash"] = 1
        formString = """
            <img src="../static/img/g-cash.jpg" alt="Girl in a jacket" width="230" height="225">
            <form action="/processPayment" method="post" style="margin-top: 10px">
                <!-- G-Cash form fields -->
                <input type="text" name="gcashField" placeholder="Enter Reference Number" class="form-control" style="max-width: 200px">
                <input type="submit" value="Submit G-Cash" name="fromGcash" class="font-monospace btn btn-primary btn-rounded btn-md mt-3">
            </form>
        """
    if formString:
        session['formString'] = formString
        
    return redirect(url_for('toCheckout'))

@app.route('/toCheckout', methods=['POST', 'GET'])
def toCheckout():
    total_amount = session.get('totalPrice')
    plusDf = total_amount+20
    
    formString = session.get('formString', "")
    print(formString)
    if total_amount==0:
        return redirect(url_for('deliverSetup'))
    
    return render_template('to-checkout.html', total_amount=total_amount, formString=formString, plusDf=plusDf)

@app.route('/deliverSetup', methods=['POST', 'GET'])
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

@app.route('/addCart', methods=["POST", "GET"])
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
    
    return redirect(url_for('deliverSetup'))

@app.route('/userPage', methods=['POST', 'GET'])
def userPage():
    return render_template("user-page.html") 

@app.route('/adminPage', methods=['POST', 'GET'])
def adminPage():
    return render_template("admin-page.html")

@app.route('/option', methods=['POST', 'GET'])
def user():
    if request.method == 'POST':
        if request.form.get('user'):
            return "user"
        elif request.form.get('admin'):
            return "admin"
    elif request.method == 'GET':
        return "get"
    return "something wrong"
    

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=3000,debug=True)