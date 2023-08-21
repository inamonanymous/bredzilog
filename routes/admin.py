from flask import Blueprint, render_template, request, redirect, url_for
import thisclass.Myclass as pnt
from werkzeug.security import generate_password_hash, check_password_hash

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin/adminPage', methods=['POST', 'GET'])
def adminPage():
    return render_template("admin-page.html")

@admin_bp.route('/admin/signedUp', methods=['POST'])
def signedUp():
    if request.method == 'POST':
        firstname = request.form.get('firstName')
        surname = request.form.get('firstName')
        email = request.form.get('email')
        phone = request.form.get('number')
        password = request.form.get('password')
        password2 = request.form.get('confirmPassword')

        if password==password2:
            new_admin = pnt.Admin(firstname, surname, email, phone, password)
            new_admin.save()
            return "NICE"

        return render_template('sign-up-page.html')
        
    return render_template('sign-up-page.html')

@admin_bp.route('/admin/signUpPage', methods=['POST', 'GET'])
def signUpPage():
    return render_template('sign-up-page.html')


@admin_bp.route('/admin/signedin', methods=['POST', 'GET'])
def signedin():
    email = request.form.get('email')
    password = request.form.get('password')

    if request.method == "POST":
        admin = pnt.Admin.get_by_email(email)
        if admin and check_password_hash(admin.password, password):
            return "hello world pasok kana"
        else: 
            return "ay mali"
    return redirect(url_for('admin.adminPage'))
