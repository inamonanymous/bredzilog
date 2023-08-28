from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import thisclass.Myclass as pnt

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/signedUp', methods=['POST'])
def signedUp():
    admin_data = pnt.AdminData()
    if request.method == 'POST':
        firstname = request.form.get('firstName')
        surname = request.form.get('surname')
        email = request.form.get('email')
        phone = request.form.get('number')
        password = request.form.get('password')
        password2 = request.form.get('confirmPassword')

        if admin_data.checkIfExists(email):
            return "email already exists"
        elif password==password2:
            new_admin = pnt.Admin(firstname, surname, email, phone, password)
            admin_data.save(new_admin)
            return redirect(url_for('admin.adminPage'))

        return render_template('sign-up-page.html')
        
    return render_template('sign-up-page.html')

@admin_bp.route('/admin/signUpPage', methods=['POST', 'GET'])
def signUpPage():
    return render_template('sign-up-page.html')

@admin_bp.route('/admin/logout', methods=['POST', 'GET'])
def logout():
    session.clear()
    return redirect(url_for('admin.adminPage'))

@admin_bp.route('/admin/dashboard', methods=['POST', 'GET'])
def dashboard():
    if 'email' in session:
        try:
            receipt_data = pnt.ReceiptsData()
            return render_template('admin-dashboard.html', receipts=receipt_data.transactions)
        except TypeError:
            return "render_template('admin-dashboard.html', receipts=list)"
    return redirect(url_for('admin.adminPage'))

@admin_bp.route('/admin/signedin', methods=['POST', 'GET'])
def signedin():
    admin_data = pnt.AdminData()
    email = request.form.get('email')
    password = request.form.get('password')
    print(admin_data.accounts)

    if request.method == "POST":
        if admin_data.loginIsTrue(email, password):
            session["email"] = email
            return redirect(url_for('admin.dashboard'))
        else: 
            return f"ay ,{admin_data.accounts} mali, "
    return redirect(url_for('admin.adminPage'))

@admin_bp.route('/admin/adminPage', methods=['POST', 'GET'])
def adminPage():
    return render_template("admin-page.html")