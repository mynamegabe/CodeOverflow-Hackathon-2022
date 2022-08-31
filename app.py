import cv2
import pytesseract
import random
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename
from PIL import Image
import os
import mysql.connector
import hashlib

app = Flask(__name__, static_url_path='/static',static_folder='static')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['FILES_FOLDER'] = 'files'
app.config['STATIC_FOLDER'] = 'static'
app.secret_key = "%032x" % random.getrandbits(128)

def sqlConnection():
    try:
        conn = mysql.connector.connect(host="localhost", user="ecoplace", password="P@ssw0rd", database="ecoplace")
        return conn
    except Exception as e:
        print(e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/businesses/<int:business_id>')
def business(business_id):
    conn = sqlConnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM businesses WHERE id = %s", (business_id,))
    business = cursor.fetchone()
    cursor.close()
    return render_template('business.html', business = business)

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/profile')
def profile():
    if 'token' in request.cookies:
        token = request.cookies.get('token')
        conn = sqlConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE token = %s", (token,))
        user = cursor.fetchone()
        cursor.close()
        return render_template('profile.html', user = user)
    else:
        return redirect(url_for('login'))

# Receipt scanning
@app.route('/scan', methods=['GET'])
def scan_receipt():
    return render_template('scan.html')

# Receipt upload
@app.route('/upload', methods=['POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        image = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], file.filename)) # not safe
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        gray = cv2.medianBlur(gray, 3)
        filename = app.config['FILES_FOLDER'] + "/receipts/" + "{}.png".format(os.getpid())
        cv2.imwrite(filename, gray)
        text = pytesseract.image_to_string(Image.open(filename))
        os.remove(filename)
        return render_template('index.html', text=text)

# AUTHENTICATION

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()
        conn = sqlConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            resp = redirect(url_for('index'))
            resp.set_cookie('token', generateToken())
            return resp
        else:
            return redirect(url_for('login'))
    else:
        return render_template('login.html')
        
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = hashlib.md5(request.form['password'].encode()).hexdigest()
        conn = sqlConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        conn.commit()
        return redirect(url_for('login'))
    else:
        return render_template('register.html')


# Admin endpoints

@app.route('/admin')
def admin():
    if checkAdmin():
        conn = sqlConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        cursor.close()
        return render_template('admin.html', users = users)
    else:
        return redirect(url_for('login'))

@app.route('/admin/businesses')
def admin_businesses():
    if checkAdmin():
        conn = sqlConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM businesses")
        businesses = cursor.fetchall()
        cursor.close()
        return render_template('admin_businesses.html', businesses = businesses)
    else:
        return redirect(url_for('login'))

@app.route('/admin/businesses/<int:business_id>')
def admin_business(business_id):
    if checkAdmin():
        conn = sqlConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM businesses WHERE id = %s", (business_id,))
        business = cursor.fetchone()
        cursor.execute("SELECT * FROM products WHERE business_id = %s", (business_id,))
        products = cursor.fetchall()
        cursor.close()
        return render_template('admin_business.html', business = business, products = products)
    else:
        return redirect(url_for('login'))

@app.route('/admin/businesses/delete/<int:business_id>', methods=['POST'])
def admin_business_delete(business_id):
    if checkAdmin():
        conn = sqlConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM businesses WHERE id = %s", (business_id,))
        conn.commit()
        cursor.close()
        return redirect(url_for('admin_businesses'))
    else:
        return redirect(url_for('login'))

@app.route('/admin/businesses/add', methods=['POST'])
def admin_business_add():
    if checkAdmin():
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            contact = request.form['contact']
            background_image = request.files['background_image']
            filename = secure_filename(background_image.filename)
            background_image.save(os.path.join(app.config['STATIC_FOLDER'], filename))
            conn = sqlConnection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("INSERT INTO businesses (name, description, contact, background_image) VALUES (%s, %s, %s, %s)", (name, description, contact, filename))
            conn.commit()
            return redirect(url_for('admin_businesses'))
        else:
            return render_template('admin_business_add.html')
    else:
        return redirect(url_for('login'))

@app.route('/admin/businesses/edit/<int:business_id>', methods=['POST'])
def admin_business_edit(business_id):
    if checkAdmin():
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            contact = request.form['contact']
            background_image = request.files['background_image']
            filename = secure_filename(background_image.filename)
            background_image.save(os.path.join(app.config['STATIC_FOLDER'], filename))
            conn = sqlConnection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("UPDATE businesses SET name = %s, description = %s, contact = %s, background_image = %s WHERE id = %s", (name, description, contact, filename, business_id))
            conn.commit()
            return redirect(url_for('admin_business', business_id = business_id))
    else:
        return redirect(url_for('login'))

@app.route('/admin/products/add/<int:business_id>', methods=['POST'])
def admin_product_add(business_id):
    if checkAdmin():
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            price = request.form['price']
            image = request.files['image']
            stock = request.form['stock']
            filename = secure_filename(image.filename)
            image.save(os.path.join(app.config['STATIC_FOLDER'], filename))
            conn = sqlConnection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("INSERT INTO products (name, description, price, image, stock, business_id) VALUES (%s, %s, %s, %s, %s, %s)", (name, description, price, filename, stock, business_id))
            conn.commit()
            return redirect(url_for('admin_business', business_id = business_id))
        else:
            return render_template('admin_product_add.html')
    else:
        return redirect(url_for('login'))

def generateToken():
    return "%032x" % random.getrandbits(128)

def checkAdmin():
    if 'token' in request.cookies:
        token = request.cookies.get('token')
        conn = sqlConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE token = %s", (token,))
        user = cursor.fetchone()
        cursor.close()
        if user["role"] == "admin":
            return True
        else:
            return False
    else:
        return False

if __name__ == "__main__":
    app.run(debug=True)