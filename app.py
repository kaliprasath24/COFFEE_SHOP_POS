from flask import Flask, render_template, request, redirect, send_file
import sqlite3
from datetime import datetime
import csv

app = Flask(__name__)

#--------------- DataBase Init----------#

def init_db():
    conn = sqlite3.connect("coffee_meet.db")
    c = conn.cursor()

    #menu tables for shop

    c.execute("""CREATE TABLE IF NOT EXISTS menu
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
               name TEXT UNIQUE,
               price REAL,
              category TEXT)""")

    #sales table for shop 

    c.execute("""CREATE TABLE IF NOT EXISTS sales
              (id INTEGER PRIMARY KEY AUTOINCREMENT,
              bill_n0 TEXT,
              item_name TEXT,
              qty INTEGER,
              price REAL,
              gst REAL,
              total REAL,
              payment_mode TEXT,
              date TEXT
              )
              """)
    
    conn.commit()
    conn.close()
init_db()


#---------------- login page --------------#
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('user')
        password = request.form.get('pass')

        if user == 'staff' and password == '1234':
            return redirect('/billing')
        else:
            return render_template('login.html', error="Invalid login")
        
    return render_template('login.html')
    

       # if request.form['user'] == 'staff' and request.form['pass'] == '1234':
        #    return redirect('/billing')
        #return render_template('login.html')
    

#------------ Billing page --------------#

@app.route('/billing')
def billing():
    conn = sqlite3.connect("coffee_meet.db")
    c = conn.cursor()

    # fetch menu items by category #

    c.execute("SELECT DISTINCT category FROM menu")
    categories = [row[0] for row in c.fetchall()]
    menu = {}
    for cat in categories:
        c.execute("SELECT name, price FROM menu WHERE category=?", (cat,))
        menu[cat] = c.fetchall()

    conn.close()
    return render_template('billing.html', menu = menu)


#--------------- saving bill ---------------#
@app.route('/save-bill', methods=['POST'])
def save_bill():
    data = request.json
    cart = data['cart']
    gst_on = data['gst']
    payment =data['payment']

    bill_no = datetime.now().strftime("%Y%m%d%H%M%S")
    date = datetime.now().strftime('%Y-%m-%d')

    conn = sqlite3.connect('coffee_meet.db')
    c = conn.cursor()

    for item, details in cart.items():
        subtotal = details['qty'] * details['price']
        gst_amt = subtotal * 0.05 if gst_on else 0 
        total = subtotal + gst_amt

        c.execute("""INSERT INTO sales(
                  bill_n0,
                  item_name,
                  qty,
                  price,
                  gst,
                  total,
                  payment_mode,
                  date) 
                  VALUES(?,?,?,?,?,?,?,?)""",
                  (bill_no,item,details['qty'],details['price'],gst_amt,total,payment,date))

    conn.commit()
    conn.close()
    return '', 204 


#-----------ADMIN page ------------#

@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    if request.method == 'POST':
        if request.form['user'] == 'admin' and request.form['pass'] == 'admin1234':
            return redirect('/dashboard')
    return render_template('admin.html')


@app.route('/dashboard')
def dashboard():
    today = datetime.now().strftime('%y-%m-%d')
    conn = sqlite3.connect('coffee_meet.db')
    c = conn.cursor()

    #----- Total Sales -----#
    c.execute("SELECT SUM(total) FROM sales WHERE date=?", (today,))
    total = c.fetchone()[0] or 0 

    #------payment mode's summary -------#
    c.execute("SELECT payment_mode, SUM(total), FROM sales WHERE date=? GROUP BY payment_mode",(today,))
    payments = c.fetchall()

    conn.close()
    return render_template('dashboard.html',total = total, payments = payments)


#------menu management -----#

@app.route('/menu', methods=['GET', 'POST'])
def menu_management():
    conn = sqlite3.connect("coffee_meet.db")
    c = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        price = request.form['price']
        category = request.form['category']
        c.execute("INSERT OR IGNORE INTO menu VALUES (NULL,?,?,?)", (name,price,category))
        conn.commit()

    c.execute("SELECT * FROM menu")
    items = c.fetchall()
    conn.close()
    return render_template('menu.html', items = items)


#------------ Sales reports ------------#

@app.route('/daily-report')
def daily_report():
    today = datetime.now().strftime('%Y-%m-%d')
    return generate_report(today)


#---------- monthly reports -----------#

@app.route('/monthly-report')
def monthly_report():
    month = datetime.now().strftime('%Y-%m')
    return generate_report(month, monthly = True)


#------- report generation -------#

def generate_report(date, monthly = False):
    conn = sqlite3.connect("coffee_meet.db")
    c = conn.cursor()
    if monthly:
        c.execute("SELECT * FROM sales WHERE date LIKE ?", (date+'%',))
    else:
        c.execute("SELECT * FROM sales WHERE date=?", (date,))
    rows = c.fetchall()
    conn.close()

    file = 'report.csv'
    with open(file, 'w', newline='') as f:
        writer = csv.writer(f)

    writer.writerow(['Bill','Item','Qty','Price','GST','Total','Payment','Date'])
    writer.writerows(rows)

    return send_file(file,as_attachment=True)
                

#----------RUNNING THE APP -----------#
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
   
    


