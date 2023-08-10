import sqlite3

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

    def getTotal(self):
        total = 0
        for i in self.list:
            for j in i:
                total += j.price
        return total

    def showList(self):
        return self.list
    
