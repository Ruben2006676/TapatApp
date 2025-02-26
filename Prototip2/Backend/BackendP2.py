from flask import Flask, request, jsonify
from datetime import date

app = Flask(__name__)

# Modelo de datos
class User:
    def __init__(self, id, username, password, email, first_name, last_name):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
    
    def to_dict(self):
        return self.__dict__

class Child:
    def __init__(self, id, user_id, name, birth_date, medical_info):
        self.id = id
        self.user_id = user_id
        self.name = name
        self.birth_date = birth_date
        self.medical_info = medical_info
    
    def to_dict(self):
        return self.__dict__

class Tap:
    def __init__(self, id, child_id, date, time, status, total_hours):
        self.id = id
        self.child_id = child_id
        self.date = date
        self.time = time
        self.status = status
        self.total_hours = total_hours
    
    def to_dict(self):
        return self.__dict__

# DAO (Data Access Object) Clases
class DAOUsers:
    def __init__(self):
        self.users = []
    
    def get_user_by_id(self, id):
        return next((u for u in self.users if u.id == id), None)
    
    def create_user(self, user):
        self.users.append(user)
        return True
    
    def update_user(self, user):
        existing_user = self.get_user_by_id(user.id)
        if existing_user:
            existing_user.username = user.username
            existing_user.password = user.password
            existing_user.email = user.email
            existing_user.first_name = user.first_name
            existing_user.last_name = user.last_name
            return True
        return False

class DAOChilds:
    def __init__(self):
        self.children = []
    
    def get_child_by_id(self, child_id):
        return next((c for c in self.children if c.id == child_id), None)
    
    def create_child(self, child):
        self.children.append(child)
        return True
    
    def update_child(self, child):
        existing_child = self.get_child_by_id(child.id)
        if existing_child:
            existing_child.name = child.name
            existing_child.birth_date = child.birth_date
            existing_child.medical_info = child.medical_info
            return True
        return False

class DAOTaps:
    def __init__(self):
        self.taps = []
    
    def get_tap_history(self, child_id):
        return [tap.to_dict() for tap in self.taps if tap.child_id == child_id]
    
    def create_tap(self, tap):
        self.taps.append(tap)
        return True
    
    def update_tap(self, tap):
        existing_tap = next((t for t in self.taps if t.id == tap.id), None)
        if existing_tap:
            existing_tap.status = tap.status
            existing_tap.total_hours = tap.total_hours
            return True
        return False

# Web Service
class WebService:
    def __init__(self):
        self.dao_users = DAOUsers()
        self.dao_childs = DAOChilds()
        self.dao_taps = DAOTaps()

    def get_user_by_id(self, id):
        user = self.dao_users.get_user_by_id(id)
        return user.to_dict() if user else None

    def get_child_by_user(self, user_id):
        return [child.to_dict() for child in self.dao_childs.children if child.user_id == user_id]

    def get_tap_history_by_user(self, user_id):
        children = self.get_child_by_user(user_id)
        tap_history = []
        for child in children:
            tap_history.extend(self.dao_taps.get_tap_history(child['id']))
        return tap_history

    def create_user(self, user):
        return self.dao_users.create_user(user)

    def create_child(self, child):
        return self.dao_childs.create_child(child)

    def create_tap(self, tap):
        return self.dao_taps.create_tap(tap)

web_service = WebService()

# Endpoints
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = web_service.get_user_by_id(data.get('id'))
    if user and user['password'] == data.get('password'):
        return jsonify({"message": "Login successful", "user": user}), 200
    return jsonify({"error": "Invalid credentials"}), 401

@app.route('/child', methods=['GET'])
def get_child():
    user_id = request.args.get('user_id', type=int)
    children = web_service.get_child_by_user(user_id)
    return jsonify(children)

@app.route('/tap/history', methods=['GET'])
def get_tap_history():
    user_id = request.args.get('user_id', type=int)
    history = web_service.get_tap_history_by_user(user_id)
    return jsonify(history)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)