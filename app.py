from flask import Flask, render_template, request, url_for, g, redirect
import sqlite3
import thisclass.Myclass as pnt

app = Flask(__name__)

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

@app.route('/deliverSetup', methods=['POST', 'GET'])
def deliverSetup():
    menu = menus.items
    my_cart = cart.showList()
    original_values = []
    prices = []
    for i in my_cart:
        for j in i:
            original_values.append(j)
            prices.append(j.price)
    
    total = sum(prices)

    return render_template('deliver-setup.html', menu=menu, original_values=original_values, total=total)

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
    print(cart.list)
    for x in cart.list:
        print(x)
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
    app.run(debug=True)