import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()
DATABASE = os.getenv('DATABASE_URL')

def checkIfInt(n):
    try:
        int_val = int(n)
        print(int_val)
        return True
    except ValueError:
        return False

class EachData:
    def __init__(self):
        self.db = DATABASE
        self.items = []
        self.fetch_from_db()
    
    def create_object(self, i):
        id, name, price, type = i
        return Item(id, name, price, type)

    def fetch_from_db(self):
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        cursor.execute('SELECT * FROM menu')
        rows = cursor.fetchall()
        for i in rows:
            obj = self.create_object(i)
            self.items.append(obj)
        connection.close()

    def get_obj_by_id(self, id):
        for i in self.items:
            if i.id == id:
                return i.name, i.price, i.type
        return None, None, None
    
    def getList(self):
        return self.items

    def __repr__(self):
        return ", ".join([str(item) for item in self.items])

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
    

class UserData:
    def __init__(self):
        self.db = DATABASE
        self.accounts = []
        self.fetch_from_db()
        

    def create_object(self, i):
        firstname, surname, email, phone, password = i
        return User(firstname, surname, email, phone, password)


    def fetch_from_db(self):
        connection = sqlite3.connect(self.db)
        cursor = connection.cursor()
        rows = cursor.fetchall()
        for i in rows:
            obj = self.create_object(i)
            self.accounts.append(obj)
        connection.close()

    def save(self, user):
        try:
            conn = sqlite3.connect(self.db)
            cursor = conn.cursor()

            cursor.execute('INSERT INTO users (name, surname, email, phone, password) VALUES (?,?,?,?,?)', 
                        (user.firstname,
                            user.surname,
                            user.email,
                            user.phone,
                            generate_password_hash(user.password),))
            
            conn.commit()
            conn.close()
        except:
            print("error saving to database")

    def loginIsTrue(self, email, password) -> bool:
        user = self.getByEmail(email)
        if user and check_password_hash(user.password, password):
            return True
        return False
    
    def getByEmail(self, email):
        for i in self.accounts:
            if i.email==email:
                user = User(i.firstname, i.surname, i.email, i.phone, "")
                user.password = i.password
                return user
        return None    

    def checkIfExists(self, email):
        for i in self.accounts:
            if i.email == email:
                return True
            return False
        
    def __repr__(self):
        return ", ".join([str(user) for user in self.accounts])

class User: 
    def __init__(self, firstname, surname, email, phone, password):
        self.firstname = firstname
        self.surname = surname
        self.email = email
        self.phone = phone
        self.password = password
        self.address = str
        self.photo = None

    def set_address(self, address):
        self.address = address

    def set_photo(self, photo):
        self.photo = photo
    

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

        cursor.execute('SELECT unique_id, name, Address, phoneNo, from_customer, referrenceNo, totalPrice FROM receipt')
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
        



