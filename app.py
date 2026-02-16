from flask import Flask, render_template, request, redirect, send_file, jsonify, url_for, session
import sqlite3
from datetime import datetime
import csv

app = Flask(__name__)
app.secret_key = "super_secret_key_123"


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
              bill_no TEXT,
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
    data = request.get_json()
    
    # safe fallback
    cart = data.get('cart', {})
    gst_on = data.get('gst', False)
    payment = data.get('payment', 'Cash')
    
    # auto-generate bill_no and date if not sent
    bill_no = data.get('bill_no') or datetime.now().strftime("%Y%m%d%H%M%S")
    date = data.get('date') or datetime.now().strftime('%Y-%m-%d')
    
    conn = sqlite3.connect('coffee_meet.db')
    c = conn.cursor()


    for item_name, details in cart.items():
        qty = details['qty']
        price = details['price']
        
        subtotal = qty * price
        gst_amt = subtotal * 0.05 if gst_on else 0
        total = subtotal + gst_amt

        c.execute(""" 
                  INSERT INTO sales (
                   bill_no,
                   item_name,
                   qty,
                   price,
                   gst,
                   total,
                   payment_mode,
                   date
                  ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                  """, (bill_no, item_name, qty, price, gst_amt, total, payment, date))



    conn.commit()
    conn.close()
    
    return jsonify({
        "status": "success",
        "bill_no": bill_no
})



#---------- print bill page ------------#
@app.route("/print-bill/<bill_no>")
def print_bill(bill_no):

    conn = sqlite3.connect("coffee_meet.db")
    c = conn.cursor()

    # Fetch bill items
    c.execute("""
        SELECT item_name, qty, price, total, payment_mode, date
        FROM sales
        WHERE bill_no = ?
    """, (bill_no,))

    rows = c.fetchall()
    conn.close()

    if not rows:
        return "Bill not found"

    bill_items = []
    payment_mode = rows[0][4]
    date = rows[0][5]
    grand_total = 0

    for row in rows:
        bill_items.append({
            "name": row[0],
            "qty": row[1],
            "price": row[2],
            "total": row[3]
        })
        grand_total += row[3]

    return render_template(
        "bill_print.html",
        bill_no=bill_no,
        date=date,
        items=bill_items,
        grand_total=grand_total,
        payment_mode=payment_mode
    )





#-----------ADMIN page ------------#

@app.route('/admin', methods = ['GET', 'POST'])
def admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "admin123":
            session["admin_logged_in"] = True
            return redirect(url_for("dashboard"))
        else:
            return render_template("admin.html", error = "invalid credentials")
        
    return render_template("admin.html") 

        


#---------- dashboard -------------#

@app.route("/dashboard")
def dashboard():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin"))

    today = datetime.now().strftime('%Y-%m-%d')
    current_month = datetime.now().strftime('%Y-%m')

    conn = sqlite3.connect("coffee_meet.db")
    c = conn.cursor()

    # ✅ Today's total sales
    c.execute("""
        SELECT COALESCE(SUM(total), 0)
        FROM sales
        WHERE date = ?
    """, (today,))
    today_total = c.fetchone()[0]

    # ✅ Monthly total sales
    c.execute("""
        SELECT COALESCE(SUM(total), 0)
        FROM sales
        WHERE date LIKE ?
    """, (current_month + "%",))
    monthly_total = c.fetchone()[0]

    # ✅ Payment mode totals (Today)
    c.execute("""
        SELECT payment_mode, COALESCE(SUM(total), 0)
        FROM sales
        WHERE date = ?
        GROUP BY payment_mode
    """, (today,))
    payment_data = c.fetchall()

    # Default values
    cash_total = 0
    upi_total = 0
    card_total = 0

    for mode, amount in payment_data:
        if mode == "Cash":
            cash_total = amount
        elif mode == "UPI":
            upi_total = amount
        elif mode == "Card":
            card_total = amount

    conn.close()

    return render_template(
        "dashboard.html",
        today_total=today_total,
        monthly_total=monthly_total,
        cash_total=cash_total,
        upi_total=upi_total,
        card_total=card_total
    )



#------------ logout route ----------------#

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("admin"))



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




#---------reports page ----------#
@app.route('/reports', methods=['GET'])
def reports():

    date = request.args.get('date')
    monthly = request.args.get('monthly')

    conn = sqlite3.connect('coffee_meet.db')
    c = conn.cursor()

    rows = []
    total_sum = 0

    if date:
        if monthly == "true":
            c.execute("SELECT * FROM sales WHERE date LIKE ?", (date + '%',))
        else:
            c.execute("SELECT * FROM sales WHERE date = ?", (date,))

        rows = c.fetchall()
        total_sum = sum(row[6] for row in rows) if rows else 0

    conn.close()

    return render_template(
        'reports.html',
        rows=rows,
        total_sum=total_sum,
        selected_date=date,
        monthly=monthly
    )





#------- report generation -------#

@app.route('/download_report')
def download_report():

    date = request.args.get('date')
    monthly = request.args.get('monthly')

    conn = sqlite3.connect('coffee_meet.db')
    c = conn.cursor()

    if monthly == "true":
        c.execute("SELECT * FROM sales WHERE date LIKE ?", (date + '%',))
    else:
        c.execute("SELECT * FROM sales WHERE date = ?", (date,))

    rows = c.fetchall()
    conn.close()

    file = "report.csv"

    with open(file, 'w', newline='') as f:
        writer = csv.writer(f)

        writer.writerow(['ID', 'bill_no', 'Item', 'Qty', 'Price', 'GST', 'Total', 'Payment', 'Date'])
        for row in rows:
            writer.writerow(row)

        total_sum = sum(row[6] for row in rows) if rows else 0
        writer.writerow([])
        writer.writerow(["", "", "", "", "", "Grand Total", total_sum])

    return send_file(file, as_attachment=True)

                

#----------RUNNING THE APP -----------#
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
   
    


