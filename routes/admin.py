from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import thisclass.Myclass as pnt
import ast

admin_bp = Blueprint('admin', __name__)

g_admin_login = None


@admin_bp.route('/admin/logout', methods=['POST', 'GET'])
def logout():
    session.pop('email', None)
    return redirect(url_for('admin.adminPage'))

@admin_bp.route('/admin/setQuantity/<id>', methods=['POST', 'GET'])
def setQuantity(id):
    if 'email' in session:
        menu = pnt.EachData()
        qty, isChecked = request.form.get(f"qty{id}"), request.form.get(f"is_enabled{id}")
        
        if int(isChecked) == 4096:
            if pnt.checkIfInt(qty):
                item = menu.get_obj_by_id(int(id))
                item.set_qty(qty)
                menu.set_qty(item)
                return redirect(url_for('admin.inventory'))
            return redirect(url_for('admin.dashboard'))
        print(isChecked)
        return redirect(url_for('admin.inventory'))

@admin_bp.route('/admin/inventory', methods=['POST', 'GET'])
def inventory():
    if 'email' in session:
        menu = pnt.EachData()
        return render_template('admin-inventory.html', menu=menu)
    return redirect(url_for('admin.adminPage'))

@admin_bp.route('/admin/updateUserSettings', methods=['POST', 'GET'])
def updateUserSettings():
    if 'email' in session and request.method == "POST" and 'user_data' in session:
        user_data = pnt.UserData()
        firstname, surname, phone, brgy, municipality, province, street, houseNo = request.form.get('firstname'), request.form.get('surname'), request.form.get('phone'), request.form.get('brgy'), request.form.get('municipality'), request.form.get('province'), request.form.get('street'), request.form.get('houseNo')
        user_acc = user_data.getByEmail(str(session.get('user_data', "")))
        user_acc.set_address(brgy, street, houseNo, municipality, province)
        user_acc.set_contact(firstname, surname, phone)

        user_data.saveAddress(user_acc)
        user_data.updateContact(user_acc)

        return redirect(url_for('admin.manageData'))

    return redirect(url_for('admin.dashboard'))
        

@admin_bp.route('/admin/update-user-id/<user_email>', methods=['POST', 'GET'])
def updateUserEmail(user_email):
    if 'email' in session:
        users = pnt.UserData()
        user = users.getByEmail(user_email)
        session['user_data'] = str(user_email)
        return render_template('admin-update-users-form.html', user=user)
    return redirect(url_for('admin.adminPage'))

@admin_bp.route('/admin/manageData', methods=['POST', 'GET'])
def manageData():
    if 'email' in session:
        users = pnt.UserData()
        return render_template('manage-data.html', accounts=users.accounts)
    return redirect(url_for('admin.adminPage'))

@admin_bp.route('/admin/updateAdminSettings', methods=['POST', 'GET'])
def adminUpdateSettings():
    g_admin_data = pnt.AdminData()
    g_admin_login = g_admin_data.getByEmail(str(session.get('email', "")))
    if 'email' in session and g_admin_login:
        name, surname, phone, email = request.form.get('name'), request.form.get('surname'), request.form.get('phone'), request.form.get('email') 
        if pnt.checkIfInt(phone):
            g_admin_login.set_contact(name, surname, phone, email)
            g_admin_data.updateAdmin(g_admin_login)
            return redirect(url_for('admin.dashboard'))
        return "incorrect phone format"
    return redirect(url_for('admin.adminPage'))

@admin_bp.route('/admin/adminSettings', methods=['POST', 'GET'])
def adminSettings():
    if 'email' in session:
        g_admin_data = pnt.AdminData()
        g_admin_login = g_admin_data.getByEmail(str(session.get('email', "")))
        return render_template('admin-settings.html', admin=g_admin_login)
    return redirect(url_for('admin.adminPage'))

@admin_bp.route('/admin/receipt/<id>', methods=['POST', 'GET'])
def receipt(id):
    receipt_data = pnt.ReceiptsData()
    receipt = receipt_data.get_by_id(int(id))

    if receipt is None:
        return redirect(url_for('admin.dashboard'))
    mylist = ast.literal_eval(receipt.item)
    return render_template('receipt.html', receipt=receipt, orders=mylist)

    
@admin_bp.route('/admin/dashboard', methods=['POST', 'GET'])
def dashboard():
    
    if 'email' in session:
        
        try:
            receipt_data = pnt.ReceiptsData()
            return render_template('admin-dashboard.html', receipts=receipt_data.transactions, sum=receipt_data.sumTotal(), users=len(pnt.UserData().accounts))
        except TypeError:
            return "render_template('admin-dashboard.html', receipts=list)"
    return redirect(url_for('admin.adminPage'))

@admin_bp.route('/admin/signedin', methods=['POST', 'GET'])
def signedin():
    g_admin_data = pnt.AdminData()
    email = request.form.get('email')
    password = request.form.get('password')
    print(g_admin_data.accounts)

    if request.method == "POST":
        if g_admin_data.loginIsTrue(email, password):
            g_admin_login = g_admin_data.getByEmail(email)
            if g_admin_login is None:
                session.pop('email', None)
                return "session expired"
            session["email"] = g_admin_login.get_email
            print(session.get('email'))
            return redirect(url_for('admin.dashboard'))
        else: 
            return f"ay ,{g_admin_data.accounts} mali, "
    return redirect(url_for('admin.adminPage'))

@admin_bp.route('/admin/adminPage', methods=['POST', 'GET'])
def adminPage():
    return render_template("admin-page.html")

