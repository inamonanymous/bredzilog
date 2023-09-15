import sqlite3
from dotenv import load_dotenv
import os
from abc import ABC

load_dotenv()
DATABASE = os.getenv('DATABASE_URL')

def checkIfInt(n):
    try:
        return int(n)
    except ValueError:
        return False

class Person(ABC):
    def __init__(self, firstname, surname, email, phone, password):
        self._firstname = firstname
        self._surname = surname
        self._email = email
        self._phone = phone
        self._password = password

    def set_id(self, id):
        try:
            self._id = id
        except:
            print('there were errors on Person.set_id(args) method')

    def set_password(self, password):
        try:
            self._password = password
        except:
            print('there were errors in Person.set_password(args) method')

    def set_contact(self, firstname, surname, phone):
        try:
            self._firstname = firstname
            self._surname = surname
            self._phone = phone
        except:
            print('there were errors in Person.set_contact(args, args*, args**) method')

    @property
    def get_id(self):
        try:
            return self._id
        except:
            print('there were errors in Person.get_id() method')
            return None

    @property
    def get_firstname(self):
        try:
            return self._firstname
        except:
            print('there were errors in Person.get_firstname() method')
            return None

    @property
    def get_surname(self):
        try:
            return self._surname
        except:
            print('there were errors in Person.get_surname() method')
            return None

    @property
    def get_email(self):
        try:
            return self._email
        except:
            print('there were errors in Person.get_email() method')
            return None

    @property
    def get_phone(self):
        try:
            return self._phone
        except:
            print('there were errors in Person.get_phone() method')
            return None

    @property
    def get_password(self):
        try:
            return self._password
        except:
            print('there were errors in Person.get_password() method')
            return None


class EachData:
    def __init__(self):
        self.db = DATABASE
        self._items = []
        self.fetch_from_db()
    
    def create_object(self, i):
        try:
            id, name, price, type, qty = i
            return Item(id, name, price, type, qty)
        except:
            print('there were errors in EachData.create_object(args) method')
            return None

    def fetch_from_db(self):
        try:
            connection = sqlite3.connect(self.db)
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM menu')
            rows = cursor.fetchall()
            for i in rows:
                obj = self.create_object(i)
                self.items.append(obj)
            connection.close()
        except:
            print('there were errors in EachData.fetch_from_db() method')

    def get_obj_by_id(self, id):
        try:
            for i in self.items:
                if i.id == id:
                    return i
            return None
        except:
            print('there were errors in EachData.get_obj_by_id() method')

    @property
    def items(self):
        try:
            return self._items
        except:
            print('there were errors in EachData.items() method')

    def set_qty(self, item):
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute('UPDATE menu SET quantity = ? WHERE id = ?', (item.qty,item.id,))
            conn.commit()
            conn.close()
        except:
            print('there were errors in EachData.set_qty(args) method')

    def decrement_qty(self, receipt):
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            for i in receipt.item:
                for j in self.items:
                    if i.id == j.id:
                        if i.qty > 0:
                            j.minus_qty()
                            cursor.execute('UPDATE menu SET quantity = ? WHERE id = ?', (j.qty, j.id))
                            conn.commit()
            conn.close()
        except:
            print('there were errors in EachData.decrement_qty')
        
    def get_item_per_type(self):
        try:
            hits = []
            afford = []
            carte = []
            add_on = []
            my_dict = {
                'hits': hits,
                'afford': afford,
                'carte': carte,
                'add_on': add_on
            }
            for i in self.items:
                if 'Zilog Hits' == i.type:
                    hits.append(i)
                elif 'Afford Mo Zilog Ko' == i.type:
                    afford.append(i)
                elif 'Sizzling Ala Carte' == i.type:
                    carte.append(i)
                elif 'add-on' == i.type:
                    add_on.append(i)
            return my_dict
        except:
            print('there were errors in EachData.get_item_per_type() method')
            return None

    def __repr__(self):
        return ", ".join([str(item) for item in self.items])


class Item:
    def __init__(self, id, name, price, type, qty):
        self._id = id
        self._name = name
        self._price = price
        self._type = type
        self._qty = qty

    @property
    def id(self):
        try:
            return self._id
        except:
            print('there were errors in Item.id() method')
            return None
    
    @property
    def name(self):
        try:
            return self._name
        except:
            print('there were errors in Item.name() method')
            return None

    @property
    def price(self):
        try:
            return self._price
        except:
            print('there were errors in Item.price() method')
            return None
    
    @property
    def type(self):
        try:
            return self._type
        except:
            print('there were errors in Item.type() method')
            return None

    @property
    def qty(self):
        try:
            return self._qty
        except:
            print('there were errors in Item.qty() method')
            return None

    def set_qty(self, qty):
        try:
            if self.qty > 0:
                self._qty = qty
        except:
            print('there were errors in Item.set_qty(args) method')                

    def minus_qty(self):
        try:
            if self.qty > 0:
                self._qty -= 1
        except:
            print('there were errors in Item.minus_qty() method')

    def __repr__(self):
        return f"{[self.id, self.name, self.price, self.type, self.qty]}"

    
class Cart:
    def __init__(self):
        self._list = []

    def addItem(self, item_id):
        try:
            for i in EachData().items:
                if i.id == item_id:
                    self._list.append(i)
                    break
        except:
            print('there were errors in Cart.addItem(arg) method')

    def deleteItem(self, item_id):
        try:
            for i in self._list:
                if i.id == item_id:
                    self._list.remove(i)
                    break
        except:
            print('there were errors in Cart.deleteItem(arg) method')
            
    def clearItems(self):
        try:
            self._list = []
        except:
            print('there were errors in Cart.clearItems() method')
    
    def getTotal(self):
        try:
            total = 0
            for i in self._list:
                total += i.price
            return total
        except:
            print('there were errors in Cart.getTotal() method')
            return None
        
    @property
    def showList(self):
        try:
            return self._list
        except:
            print('there were errors in Cart.showList() method')
            return None


from werkzeug.security import generate_password_hash, check_password_hash
class AdminData:
    def __init__(self):
        self.db = DATABASE
        self.accounts = []
        self.fetch_from_db()

    def create_object(self, i):
        try:
            firstname, surname, email, phone, password = i
            return Admin(firstname, surname, email, phone, password)
        except:
            print('there were errors in AdminData.create_object(args) method')
            return None

    def fetch_from_db(self):
        try:
            connection = sqlite3.connect(self.db)
            cursor = connection.cursor()
            cursor.execute('SELECT name, surname, email, phoneNo, password FROM admin')
            rows = cursor.fetchall()
            for i in rows:
                obj = self.create_object(i)
                self.accounts.append(obj)
            connection.close()
        except:
            print('there were errors in AdminData.fetch_from_db() method')
        
    def loginIsTrue(self, email, password) -> bool:
        try:
            admin = self.getByEmail(email)
            return admin and check_password_hash(admin.get_password, password)
        except:
            print('there were errors in AdminData.loginIsTrue(args, args**) method')
            return False

    def updateAdmin(self, admin):
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute('UPDATE admin SET name = ?, surname = ?, email = ?, phoneNo = ?', (admin.get_firstname,
                                                                                                            admin.get_surname,
                                                                                                            admin.get_email,
                                                                                                            admin.get_phone,))
            conn.commit()
            conn.close()
        except:
            print('there were errors in AdminData.create_object(args) method')

    """def save(self, admin):
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
            print("error saving to database")"""

    def getByEmail(self, email):
        try:
            for i in self.accounts:
                if i.get_email==email:
                    admin = Admin(i.get_firstname, i.get_surname, i.get_email, i.get_phone, "")
                    admin.set_password(i.get_password) 
                    return admin
            return None
        except:
            print('there were errors in AdminData.getByEmail(args) method')
            return None

    def checkIfExists(self, email):
        try:
            for i in self.accounts:
                if i.email == email:
                    return True
                return False
        except:
            print('there were errors in AdminData.checkIfExists(args) method')
            return False

    def __repr__(self):
        return ", ".join([str(admin) for admin in self.accounts])
    

class Admin(Person):
    def __init__(self, firstname, surname, email, phone, password):
        super().__init__(firstname, surname, email, phone, password)
        
    def set_contact(self, firstname, surname, phone, email):
        try:
            self._firstname = firstname
            self._surname = surname
            self._phone = phone
            self._email = email
        except:
            print('there were errors in Admin.set_contact(args, args*, args**, args***) method')
            
    def __repr__(self) -> str:
        return f"({self.get_firstname},{self.get_surname},{self.get_email},{self.get_phone},{self.get_password})"  
    

import json
class UserData:
    def __init__(self):
        self.db = DATABASE
        self.accounts = []
        self.fetch_from_db()
        
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
            print('there were errors in UserData.fetch_from_db() method')

    def save(self, user):
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO users (name, surname, email, phone, password) VALUES (?,?,?,?,?)', 
                        (str(user.get_firstname).strip(),
                            str(user.get_surname).strip(),
                            str(user.get_email).strip(),
                            str(user.get_phone).strip(),
                            generate_password_hash(user.get_password),))
            conn.commit()
            conn.close()
        except:
            print("there were errors in UserData.save(arg) method")

    def updatePassword(self, user):
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET password = ? WHERE email = ?',
                            (generate_password_hash(user.get_password),
                            user.get_email),)
            conn.commit()
            conn.close()
            self.fetch_from_db()
        except:
            print('there were errors in UserData.updatePassword(arg) method')
    
    def updateContact(self, user):
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute('UPDATE users SET name = ?, surname = ?, phone = ? WHERE email = ?', (user.get_firstname, user.get_surname, user.get_phone, user.get_email))
            conn.commit()
            conn.close()
            self.fetch_from_db()
        except:
            print('there were errors in UserData.updateContact(arg) method')

    def saveAddress(self, user):
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            address = json.dumps(user.get_address)
            cursor.execute('UPDATE users SET address = ? WHERE email = ?', (address, user.get_email,))
            conn.commit()
            conn.close()
            self.fetch_from_db()
        except:
            print('there were errors in UserData.saveAddress(arg) method')
        
    def loginIsTrue(self, email, password) -> bool:
        try:
            user = self.getByEmail(email)
            return user and check_password_hash(user.get_password, password)
        except:
            print('there were errors in UserData.loginIsTrue(arg, arg*) method')
            return False    
    
    def getByEmail(self, email):
        try:
            for i in self.accounts:
                if i.get_email==email:
                    user = User(i.get_firstname, i.get_surname, i.get_email, i.get_phone, "")
                    address_obj = i.get_address
                    brgy, houseNo, street, municipality, province = address_obj['brgy'], address_obj['houseNo'], address_obj['street'], address_obj['municipality'], address_obj['province']
                    user.set_password(i.get_password)
                    user.set_id(i.get_id)
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
            return False  
        
    def __repr__(self):
        return ", ".join([str(user) for user in self.accounts])

class User(Person): 
    def __init__(self, firstname: str = None, surname=None, email=None, phone=None, password=None):
        super().__init__(firstname, surname, email, phone, password)
        self._id = int
        self._address = {'brgy': None, 
                        'houseNo': None,
                        'street': None,
                        'municipality': None,
                        'province': None
                        }
        self._photo = None
        

    def set_address(self, brgy, street, houseNo, municipality, province):
        try:
            self._address = {'brgy': str(brgy),
                            'houseNo': str(street),
                            'street': str(houseNo),
                            'municipality': str(municipality),
                            'province': str(province)
                            }
        except:
            print('there were errors in User.set_address(arg, arg*, arg**, arg***, arg****) method')

    def set_photo(self, photo):
        try:
            self._photo = photo
        except:
            print('there were errors in User.set_photo(arg) method')

    def set_password(self, password):
        try:
            self._password = password
        except:
            print('there were errors in User.set_password(arg) method')

    @property
    def get_address(self):
        try:
            return self._address
        except:
            print('there were errors in User.get_address() method')
            return None
    
    def check_address_null(self):
        try:
            return all(value != 'None' for value in self._address.values())
        except:
            print('there were errors in User.check_address_null() method')
            return None

    @property        
    def get_per_address(self):
        try:
            if any(value is None for value in self._address.values()):
                return None, None, None, None, None
            return self._address['brgy'], self._address['houseNo'], self._address['street'], self._address['municipality'], self._address['province']
        except:
            print('there were errors in User.get_per_address() method')
            return None

    def get_photo(self):
        try:
            return self._photo
        except:
            print('there were errors in User.photo() method')
            return None

    def __repr__(self) -> str:
        return f"ID: {self.get_id}, Firstname : {self.get_firstname}, Surname: {self.get_surname}, Email: {self.get_email}, Phone: {self.get_phone}, Address: {self.get_address}"


import uuid
import random
import time
class ReceiptsData:
    def __init__(self):
        self.db = DATABASE
        self.transactions = []
        self.fetch_from_database()

    def create_object(self, i):
        try:
            id, unique, name, address, phone, from_customer, referrenceNo, totalPrice, item, isDineIn = i
            return Receipts(id, unique, name, address, phone, from_customer, referrenceNo, totalPrice, item)
        except:
            print('there were errors in ReceiptsData.create_object() method')
            return None

    def fetch_from_database(self):
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute('SELECT id, unique_id, name, Address, phoneNo, from_customer, referrenceNo, totalPrice, item, isDineIn FROM receipt ORDER BY id DESC')
            rows = cursor.fetchall()
            for i in rows:
                obj = self.create_object(i)
                obj.isDineIn=i[9]
                self.transactions.append(obj)
            conn.close()
        except:
            print('there were errors in ReceiptsData.fetch_from_database() method')

    @staticmethod
    def generate_unique_id() -> str:
        try:
            timestamp = int(time.time()*1000)
            random_number = random.randint(0,999)
            unique_id = uuid.uuid4().hex
            final_id = f"{timestamp:013d}{random_number:03d}{unique_id[:9]}"
            return final_id
        except:
            print('there were errors in ReceiptsData.generate_unique_id() static method')
            return None

    def get_by_id(self, id):
        try:
            for i in self.transactions:
                if i.id == id:
                    return i
            return None
        except:
            print('there were errors in ReceiptsData.get_by_id(args) method')
            return None

    def save_to_db(self, receipt):
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO receipt (unique_id, name, Address, phoneNo, from_customer, referrenceNo, totalPrice, item, isDineIn) VALUES (?,?,?,?,?,?,?,?,?)', 
                        (receipt.unique,
                        receipt.name,
                        receipt.address,
                        receipt.phone,
                        receipt.from_customer,
                        receipt.referrenceNo,
                        receipt.price,
                        str(receipt.item),
                        receipt.isDineIn,))
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
            print('there were errors in ReceiptsData.sumTotal() method')
            return -1


class Receipts:
    def __init__(self, id, unique, name, address, phone, from_customer, referrenceNo, price, item):
        self.db = DATABASE
        self.id = id
        self.unique = unique
        self.name = name
        self.address = address
        self.phone = phone
        self.from_customer = from_customer
        self.referrenceNo = referrenceNo
        self.price = price
        self.item = item
        self.isDineIn = int

    def __repr__(self) -> str:
        return f"""
                {self.unique},
                {self.name},
                {self.address},
                {self.phone},
                {self.from_customer},
                {self.referrenceNo},
                {self.price},
                {self.item}
                """
        



