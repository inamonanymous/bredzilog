from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import thisclass.Myclass as pnt

admin_bp = Blueprint('admin', __name__)

g_admin_login = None


@admin_bp.route('/admin/logout', methods=['POST', 'GET'])
def logout():
    session.pop('email', None)
    return redirect(url_for('admin.adminPage'))

@admin_bp.route('/admin/inventory', methods=['POST', 'GET'])
def inventory():
    if 'email' in session:
        return render_template('admin-inventory.html', menu=pnt.EachData())
    return redirect(url_for('admin.adminPage'))

@admin_bp.route('/admin/updateUserSettings', methods=['POST', 'GET'])
def updateUserSettings():
    if 'email' in session:
        firstname, surname, email, phone, brgy, municipality, province, street, houseNo = request.form.get('firstname'), request.form.get('surname'), request.form.get('email'), request.form.get('phone'), request.form.get('brgy'), request.form.get('municipality'), request.form.get('province'), request.form.get('street'), request.form.get('houseNo')
        if request.method == "POST":
            pass

    return redirect(url_for('admin.adminPage'))
        

@admin_bp.route('/admin/update-user-id/<user_email>', methods=['POST', 'GET'])
def updateUserEmail(user_email):
    if 'email' in session:
        users = pnt.UserData()
        user = users.getByEmail(user_email)

        return render_template('admin-update-users-form.html', user=user)
    return redirect(url_for('main.index'))

@admin_bp.route('/admin/manageData', methods=['POST', 'GET'])
def manageData():
    if 'email' in session:
        users = pnt.UserData()
        return render_template('manage-data.html', accounts=users.accounts)
    return redirect(url_for('admin.adminPage'))

@admin_bp.route('/admin/dashboard', methods=['POST', 'GET'])
def dashboard():
    g_admin_data = pnt.AdminData()
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

