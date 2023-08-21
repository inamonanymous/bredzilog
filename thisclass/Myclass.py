import sqlite3
from dotenv import load_dotenv
import os
from werkzeug.security import generate_password_hash, check_password_hash

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
    def __init__(self, db):
        self.db = db
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
        return f"{self.items[0]}, {self.items[1]}, {self.items[2]}, {self.items[3]} "

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


class Admin:
    def __init__(self, firstname, surname, email, phone, password):
        self.firstname = firstname
        self.surname = surname
        self.email = email
        self.phone = phone
        self.password = generate_password_hash(password)

    def save(self):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute('INSERT INTO admin (name, surname, email, phoneNo, password) VALUES (?,?,?,?,?)',(self.firstname, self.surname, self.email, self.phone, self.password,))
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_email(email):
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM admin WHERE email = ?', (email,))
        row = cursor.fetchone()

        conn.close()

        if row:
            admin = Admin(row[1], row[2], row[3], row[4], "")
            admin.password = row[5]
            return admin
        return None


    
