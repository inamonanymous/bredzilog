import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE = os.getenv('DATABASE_URL')

"""
    return true if input is int
"""
def checkIfInt(n):
    try:
        return int(n)
    except TypeError:
        return False


"""
    Each Data from DATABASE `menus` TABLE instantiated `Item`
      object TO `EachData.items` LIST attribute
"""
class EachData:
    def __init__(self):
        self.db = DATABASE
        self.items = []
        self.fetch_from_db()
    
    """
        Unpack values from `i` and make those values
        as arguments creating an instance of
        `Item` class
    """
    def create_object(self, i):
        id, name, price, type = i
        return Item(id, name, price, type)

    """
        Fetch all data from `menus` TABLE in DATABASE
        and for each row use `create_object(i)` function
        to return each instance of `Item's` class using
        `menus` columns for each argument.
    """
    def fetch_from_db(self):
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM menu')
        rows = cursor.fetchall()
        for i in rows:
            obj = self.create_object(i)
            self.items.append(obj)
        connection.close()

    """
        Return `Item` object attributes: 
        ('name',
        'price',
        'type')
         based from what id is received 
    """
    def get_obj_by_id(self, id):
        for i in self.items:
            if i.id == id:
                return i.name, i.price, i.type
        return None, None, None
    
    """
        return `items` attribute that
        contains `Item` class instance that 
        fetched from database
    """
    def getList(self):
        return self.items


    """
        String representation of this object.
    """
    def __repr__(self):
        return ", ".join([str(item) for item in self.items])


"""
    `Items` class that almost always rely
      to `EachData` class 
"""
class Item:
    def __init__(self, id, name, price, type):
        self.id = id
        self.name = name
        self.price = price
        self.type = type

    def getId(self):
        return self.id

    def getName(self):
        return self.name

    def getPrice(self):
        return self.price
    
    def getType(self):
        return self.type

    def __repr__(self):
        return f"{[self.id, self.name, self.price, self.type]}"

    
class Cart:
    def __init__(self):
        self.list = []

    def addItem(self, items):
        self.list.append([items])

    def deleteItem(self, item_id):
        isFound = False
        #O(n*m)
        for i in self.list:
            for j in i:
                if j.id == item_id:
                    isFound = True
                    self.list.remove(i)
                    break
            if isFound:
                break
        
    
    def getTotal(self):
        total = 0
        for i in self.list:
            for j in i:
                total += j.price
        return total

    def showList(self):
        return self.list

from werkzeug.security import generate_password_hash, check_password_hash
class AdminData:
    def __init__(self):
        self.db = DATABASE
        self.accounts = []
        self.fetch_from_db()

    def create_object(self, i):
        firstname, surname, email, phone, password = i
        return Admin(firstname, surname, email, phone, password)
    
    def fetch_from_db(self):
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        cursor.execute('SELECT name, surname, email, phoneNo, password FROM admin')
        rows = cursor.fetchall()
        for i in rows:
            obj = self.create_object(i)
            self.accounts.append(obj)
        connection.close()

    def loginIsTrue(self, email, password) -> bool:
        admin = self.getByEmail(email)
        if admin and check_password_hash(admin.password, password):
            return True
        return False


    def save(self, admin):
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()

            cursor.execute('INSERT INTO admin (name, surname, email, phoneNo, password) VALUES (?,?,?,?,?)',
                        (admin.firstname, 
                            admin.surname, 
                            admin.email, 
                            admin.phone, 
                            generate_password_hash(admin.password),))
            conn.commit()
            conn.close()
        except:
            print("error saving to database")

    def getByEmail(self, email):
        for i in self.accounts:
            if i.email==email:
                admin = Admin(i.firstname, i.surname, i.email, i.phone, "")
                admin.password = i.password
                return admin
        return None

    def checkIfExists(self, email):
        for i in self.accounts:
            if i.email == email:
                return True
            return False

    def __repr__(self):
        return ", ".join([str(admin) for admin in self.accounts])
    

class Admin:
    def __init__(self, firstname, surname, email, phone, password):
        self.firstname = firstname
        self.surname = surname
        self.email = email
        self.phone = phone
        self.password = password
        
    
    def __repr__(self) -> str:
        return f"({self.firstname},{self.surname},{self.email},{self.phone},{self.password})"  
    
import json
class UserData:
    def __init__(self):
        self.db = DATABASE
        self.accounts = []
        self.fetch_from_db()
        
##################################################################
    def create_object(self, i):
        try:
            id, firstname, surname, email, phone, password, photo, address = i
            user = User(firstname, surname, email, phone, password)
            if len(str(address)) == 0 or address is None:
                user.set_id(id)
                user.set_photo(photo)
                return user
            address_obj = json.loads(address)
            brgy, houseNo, street, municipality, province = address_obj['brgy'], address_obj['houseNo'], address_obj['street'], address_obj['municipality'] ,address_obj['province']
            user.set_address(brgy, houseNo, street, municipality, province)
            user.set_id(id)
            user.set_photo(photo)
            return user
        except:
            print('there were errors in UserData.create_object() method')


    def fetch_from_db(self):
        try:
            connection = sqlite3.connect(self.db)
            cursor = connection.cursor()
            rows = cursor.execute('SELECT * FROM users')
            for i in rows:
                obj = self.create_object(i)
                self.accounts.append(obj)
            connection.close()
        except:
            print('there were errors in UserData.fetch)_from_fb() method')

    def save(self, user):
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()

            cursor.execute('INSERT INTO users (name, surname, email, phone, password) VALUES (?,?,?,?,?)', 
                        (user.get_firstname(),
                            user.get_surname(),
                            user.get_email(),
                            user.get_phone(),
                            generate_password_hash(user.get_password()),))
            
            conn.commit()
            conn.close()
            self.fetch_from_db()
        except:
            print("there were errors in UserData.save(arg) method")

    
    def saveAddress(self, user):
            try:
                conn = sqlite3.connect(self.db)
                cursor = conn.cursor()
                address = json.dumps(user.get_address())
                cursor.execute('UPDATE users SET address = ? WHERE email = ?', (address, user.get_email(),))
                
                conn.commit()
                conn.close()
                self.fetch_from_db()
            except:
                print('there were errors in UserData.saveAddress(arg) method')
        

    def loginIsTrue(self, email, password) -> bool:
        try:
            user = self.getByEmail(email)
            return user and check_password_hash(user.get_password(), password)
        except:
            print('there were errors in UserData.loginIsTrue(arg, arg*) method')    
    
    def getByEmail(self, email):
        try:
            for i in self.accounts:
                if i.get_email()==email:
                    user = User(i.get_firstname(), i.get_surname(), i.get_email(), i.get_phone(), "")
                    address_obj = i.get_address()
                    brgy, houseNo, street, municipality, province = address_obj['brgy'], address_obj['houseNo'], address_obj['street'], address_obj['municipality'], address_obj['province']
                    user.set_password(i.get_password())
                    user.set_id(i.get_id())
                    user.set_address(brgy, houseNo, street, municipality, province)
                    return user
        except:
            print('there were error in UserData.getbyEmail(arg) method')
            return None    

    def checkIfExists(self, email) -> bool:
        try:
            for i in self.accounts:
                return i.get_email() == email
        except:
            print('there were errors in UserData.checkIfExists(arg) method')    
        
    def __repr__(self):
        return ", ".join([str(user) for user in self.accounts])

class User: 
    def __init__(self, firstname, surname, email, phone, password):
        self._id = int
        self._firstname = firstname
        self._surname = surname
        self._email = email
        self._phone = phone
        self._password = password
        self._address = {'brgy': None, 
                        'street': None,
                        'houseNo': None,
                        'municipality': None,
                        'province': None
                        }
        self._photo = None
        

    def set_id(self, id):
        self._id = id

    def set_address(self, brgy, street, houseNo, municipality, province):
        self._address = {'brgy': str(brgy),
                        'street': str(street),
                        'houseNo': str(houseNo),
                        'municipality': str(municipality),
                        'province': str(province)
                        }

    def set_photo(self, photo):
        self._photo = photo
    
    def set_password(self, password):
        self._password = password

    def get_id(self):
        return self._id

    def get_firstname(self):
        return self._firstname

    def get_surname(self):
        return self._surname
    
    def get_email(self):
        return self._email
    
    def get_phone(self):
        return self._phone
    
    def get_password(self):
        return self._password
    
    def get_address(self):
        return self._address
    
    def get_per_address(self):
        if any(value is None for value in self._address.values()):
            return None, None, None, None, None

        return self._address['brgy'], self._address['street'], self._address['houseNo'], self._address['municipality'], self._address['province']
    
    def get_photo(self):
        return self._photo
    
    def __repr__(self) -> str:
        return f"ID: {self.get_id()}, Firstname : {self.get_firstname()}, Surname: {self.get_surname()}, Email: {self.get_email()}, Phone: {self.get_phone()}, Address: {self.get_address()}"

import uuid
import random
import time
class ReceiptsData:
    def __init__(self):
        self.db = DATABASE
        self.transactions = []
        self.fetch_from_database()

    def create_object(self, i):
        unique, name, address, phone, from_customer, referrenceNo, totalPrice = i
        return Receipts(unique, name, address, phone, from_customer, referrenceNo, totalPrice)

    def fetch_from_database(self) -> list:
        conn = sqlite3.connect(self.db)
        cursor = conn.cursor()

        cursor.execute('SELECT unique_id, name, Address, phoneNo, from_customer, referrenceNo, totalPrice FROM receipt ORDER BY id DESC')
        rows = cursor.fetchall()

        for i in rows:
            obj = self.create_object(i)
            self.transactions.append(obj)
        conn.close()

    @staticmethod
    def generate_unique_id() -> str:
        timestamp = int(time.time()*1000)
        random_number = random.randint(0,999)
        unique_id = uuid.uuid4().hex
        final_id = f"{timestamp:013d}{random_number:03d}{unique_id[:9]}"

        return final_id


    def save_to_db(self, receipt):
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            
            cursor.execute('INSERT INTO receipt (unique_id, name, Address, phoneNo, from_customer, referrenceNo, totalPrice) VALUES (?,?,?,?,?,?,?)', 
                        (receipt.unique,
                        receipt.name,
                        receipt.address,
                        receipt.phone,
                        receipt.from_customer,
                        receipt.referrenceNo,
                        receipt.price,))
            conn.commit()
            conn.close()
        except sqlite3.IntegrityError:
            print("can't add null values to strict data")

    def sumTotal(self):
        try:
            sum = 0
            for i in self.transactions:
                sum = sum+int(i.price)
            return sum
        except:
            return -1


class Receipts:
    def __init__(self, unique, name, address, phone, from_customer, referrenceNo, price):
        self.db = DATABASE
        self.unique = unique
        self.name = name
        self.address = address
        self.phone = phone
        self.from_customer = from_customer
        self.referrenceNo = referrenceNo
        self.price = price

    def __repr__(self) -> str:
        return f"""
                {self.unique},
                {self.name},
                {self.address},
                {self.phone},
                {self.from_customer},
                {self.referrenceNo},
                {self.price}
                """
        



