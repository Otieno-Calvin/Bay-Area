from flask import Flask, render_template, request, session
import random
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'

DATABASE_PATH = "C:/Users/Jeremy/Pictures/Camera Roll/Bay_Area/delivery.db"

def init_database():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            id_no TEXT NOT NULL,
            package_type TEXT NOT NULL,
            payment_method TEXT NOT NULL,
            transaction_code TEXT NOT NULL,
            delivery_from TEXT,
            delivery_to TEXT,
            distance REAL
        )
    ''')
    conn.commit()
    conn.close()

init_database()

DISTANCES = {
    ('Nairobi', 'Mombasa'): 500,
    ('Nairobi', 'Kisumu'): 300,
}

def generate_order_id():
    return 'AOUG' + ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=8))

def calculate_distance(delivery_from, delivery_to):
    predefined_distance = DISTANCES.get((delivery_from, delivery_to))
    if predefined_distance is not None:
        return predefined_distance
    return 0

@app.route('/', methods=['GET', 'POST'])
def submit_personal_info():
    if request.method == 'POST':
        name = request.form['name']
        id_no = request.form['id_no']
        package_type = request.form['goods']
        payment_method = request.form['payment']
        order_id = generate_order_id()
        session['order_info'] = {
            'order_id': order_id,
            'name': name,
            'id_no': id_no,
            'package_type': package_type,
            'payment_method': payment_method,
        }
        return render_template('location_form.html', order_info=session['order_info'])
    return render_template('personal_info.html')

@app.route('/submit_location', methods=['POST'])
def submit_location():
    if request.method == 'POST':
        if 'order_info' in session:
            order_info = session['order_info']
            if 'firstDropdown' in request.form and 'secondDropdown' in request.form:
                delivery_from = request.form['firstDropdown']
                delivery_to = request.form['secondDropdown']
                distance = calculate_distance(delivery_from, delivery_to)
                order_id = generate_order_id()
                order_info['delivery_from'] = delivery_from
                order_info['delivery_to'] = delivery_to
                order_info['order_id'] = order_id
                order_info['distance'] = distance
                total_cost = distance * 10
                order_info['total_cost'] = total_cost
                session['order_info'] = order_info
                return render_template('payment.html', order_info=order_info)
        else:
            return "Error: 'order_info' not found in session"
    return "Error: Invalid request"

@app.route('/submit_payment', methods=['POST'])
def submit_payment():
    if request.method == 'POST':
        if 'order_info' in session:
            order_info = session['order_info']
            transaction_code = request.form['transaction_code']
            order_info['transaction_code'] = transaction_code  # Add transaction_code to order_info
            print("Order Info:", order_info)
            print("Transaction Code:", transaction_code)
            save_order_to_database(order_info)
            session.pop('order_info', None)
            print("Order saved to the database")
            return render_template('thank_you.html', order_id=order_info['order_id'])
    print("Error: Invalid request method or missing order_info in the session")
    return "Error: Invalid request method or missing order_info in the session"

def save_order_to_database(order_info):
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO orders (order_id, name, id_no, package_type, payment_method, transaction_code,
                            delivery_from, delivery_to, distance)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (order_info['order_id'], order_info['name'], order_info['id_no'],
          order_info['package_type'], order_info['payment_method'], order_info['transaction_code'],
          order_info['delivery_from'], order_info['delivery_to'], order_info['distance']))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    app.run(debug=True)