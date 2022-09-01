import cv2
import pytesseract
import random
from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file
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
pytesseract.pytesseract.tesseract_cmd = r'C:\\Users\\Gabriel\Desktop\\Competitions\\SIT Code Overflow 2022\\CodeOverflow-Hackathon-2022\\tesseract\\tesseract.exe'

def sqlConnection():
    try:
        conn = mysql.connector.connect(host="localhost", user="ecoplace", password="P@ssw0rd", database="ecoplace")
        return conn
    except Exception as e:
        print(e)

@app.route('/')
def index():
    conn = sqlConnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM businesses LIMIT 3")
    businesses = cursor.fetchall()
    cursor.close()
    return render_template('index.html', businesses=businesses)

@app.route('/business/<int:business_id>')
def business(business_id):
    conn = sqlConnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM businesses WHERE business_id = %s", (business_id,))
    business = cursor.fetchone()
    business['tags'] = business['categories'].split(',')
    cursor.close()
    return render_template('business.html', business = business)

@app.route('/shop')
def shop():
    conn = sqlConnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM businesses")
    businesses = cursor.fetchall()
    cursor.close()
    
    featured = [ businesses[i] for i in random.sample(range(len(businesses)), 3) ]
    food = [ business for business in businesses if "food" in business['categories'].lower() ]
    care = [ business for business in businesses if "care" in business['categories'].lower() ]
    return render_template('shop.html', food=food, featured=featured, care=care)


@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/redeem')
def redeem():
    return render_template('redeem.html')

@app.route('/profile')
def profile():
    if 'token' in request.cookies:
        token = request.cookies.get('token')
        conn = sqlConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE session = %s", (token,))
        user = cursor.fetchone()
        cursor.close()
        return render_template('profile.html', user = user)
    else:
        return redirect(url_for('login'))

# Receipt scanning
@app.route('/scan-receipts', methods=['POST'])
def scan_receipt():
    if request.method == 'POST':
        if 'receipt' not in request.files:
            return redirect(request.url)
        file = request.files['receipt']
        if file:
            # generate random filename
            filename = "%032x" % random.getrandbits(128) + ".png"
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img = cv2.imread(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            text = pytesseract.image_to_string(img)
            print(text)
            conn = sqlConnection()
            cursor = conn.cursor(dictionary=True)
            uid = request.cookies.get('token')
            cursor.execute("INSERT INTO receipts (uid, file, extracted_text) VALUES (%s, %s, %s)", (uid, filename, text))
            conn.commit()
            cursor.close()
            resp = redirect(url_for('redeem'))
            return resp

    else:
        return render_template('scan-receipts.html')
        

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
            resp.set_cookie('token', user['session'])
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
        token = generateToken()
        conn = sqlConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("INSERT INTO users (username, email, password, session) VALUES (%s, %s, %s, %s)", (username, email, password, token))
        conn.commit()
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

@app.route('/rewards')
def rewards():
    conn = sqlConnection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM rewards")
    rewards = cursor.fetchall()
    cursor.execute("SELECT points FROM users WHERE session = %s", (request.cookies.get('token'),))
    points = cursor.fetchone()['points']
    cursor.close()
    return render_template('rewards.html', rewards=rewards, points=points)



# Admin endpoints

@app.route('/admin')
def admin():
    if checkAdmin():
        conn = sqlConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT count(uid) AS c FROM users")
        users = cursor.fetchone()
        cursor.execute("SELECT count(business_id) AS c FROM businesses")
        businesses = cursor.fetchone()
        cursor.execute("SELECT count(product_id) AS c FROM products")
        products = cursor.fetchone()
        cursor.close()
        print(products)
        return render_template('admin_dashboard.html', users = users, businesses = businesses, products = products)
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
        cursor.execute("SELECT * FROM businesses WHERE business_id = %s", (business_id,))
        business = cursor.fetchone()
        cursor.execute("SELECT * FROM products WHERE business_id = %s", (business_id,))
        products = cursor.fetchall()
        cursor.close()
        return render_template('admin_business.html', business = business, products = products)
    else:
        return redirect(url_for('login'))

@app.route('/admin/businesses/delete/<int:business_id>', methods=['GET', 'POST'])
def admin_business_delete(business_id):
    if checkAdmin():
        conn = sqlConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("DELETE FROM businesses WHERE business_id = %s", (business_id,))
        conn.commit()
        cursor.close()
        return redirect(url_for('admin_businesses'))
    else:
        return redirect(url_for('login'))

@app.route('/admin/businesses/add', methods=['GET', 'POST'])
def admin_business_add():
    if checkAdmin():
        if request.method == 'POST':
            name = request.form['name']
            description = request.form['description']
            contact = request.form['contact']
            background_image = request.files['background_image']
            logo = request.files['logo_image']
            main_category = request.form['category']
            categories = request.form['categories']
            benefit = request.form['benefit']
            url = request.form['url']
            filename = secure_filename(background_image.filename)
            background_image.save(os.path.join(app.config['STATIC_FOLDER'], 'img/business/', filename))
            filename2 = secure_filename(logo.filename)
            logo.save(os.path.join(app.config['STATIC_FOLDER'], 'img/business/', filename2))
            conn = sqlConnection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("INSERT INTO businesses (name, description, contact, background_image, logo_image, main_category, categories, benefit, url) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (name, description, contact, filename, filename2, main_category, categories, benefit, url))
            conn.commit()
            return redirect(url_for('admin_businesses'))
        else:
            return render_template('admin_businesses_add.html')
    else:
        return redirect(url_for('login'))

@app.route('/admin/businesses/edit/<int:business_id>', methods=['GET','POST'])
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

@app.route('/admin/receipts')
def admin_receipts():
    if checkAdmin():
        conn = sqlConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM receipts")
        receipts = cursor.fetchall()
        cursor.close()
        return render_template('admin_receipts.html', receipts = receipts)
    else:
        return redirect(url_for('login'))

@app.route('/admin/receipts/approve/<int:rid>/<int:points>', methods=['GET'])
def admin_receipts_approve(rid, points):
    if checkAdmin():
            session = request.cookies.get('token')
            conn = sqlConnection()
            cursor = conn.cursor(dictionary=True)
            cursor.execute("UPDATE receipts SET approved = 1, points = %s WHERE receipt_id = %s", (points, rid,))
            cursor.execute("UPDATE users SET points = points + %s WHERE session = %s", (points, session,))
            conn.commit()
            cursor.close()
            return redirect(url_for('admin_receipts'))
    else:
        return redirect(url_for('login'))

@app.route('/admin/receipts/<int:receipt_id>')
def admin_receipt(receipt_id):
    if checkAdmin():
        conn = sqlConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT file FROM receipts WHERE receipt_id = %s", (receipt_id,))
        receiptimage = cursor.fetchone()
        cursor.close()
        return send_file(os.path.join(app.config['UPLOAD_FOLDER'], receiptimage['file']), mimetype='image/png')
    else:
        return redirect(url_for('login'))


def generateToken():
    return "%032x" % random.getrandbits(128)

def checkAdmin():
    if 'token' in request.cookies:
        token = request.cookies.get('token')
        conn = sqlConnection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE session = %s", (token,))
        user = cursor.fetchone()
        cursor.close()
        if user["role"] == "admin":
            return True
        else:
            return False
    else:
        return False


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)