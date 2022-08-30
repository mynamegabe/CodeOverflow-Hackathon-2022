import cv2
import pytesseract
import random
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
from PIL import Image
import os
import mysql.connector

app = Flask(__name__, static_url_path='',static_folder='static')
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['FILES_FOLDER'] = 'files'
app.secret_key = "%032x" % random.getrandbits(128)

def sqlConnection():
    try:
        conn = mysql.connector.connect(host="localhost", user="root", password="", database="ecology")
        return conn
    except:
        print("Connection Failed")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/businesses/<int:business_id>')
def business(business_id):
    conn = sqlConnection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM businesses WHERE id = %s", (business_id,))
    business = cursor.fetchone()
    cursor.close()
    return render_template('business.html', business = business)

@app.route('/cart')
def cart():
    return render_template('cart.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

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
        password = request.form['password']
        conn = sqlConnection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s", (username, password))
        user = cursor.fetchone()
        if user:
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    else:
        return render_template('login.html')
        
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlConnection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return redirect(url_for('login'))
    else:
        return render_template('register.html')

if __name__ == "__main__":
    app.run(debug=True)