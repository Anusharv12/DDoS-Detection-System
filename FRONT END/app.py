
from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

app = Flask(__name__)
app.secret_key = 'your_secure_random_key_123'  # Replace with a secure key
app.config['UPLOAD_FOLDER'] = 'uploads'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# MySQL connection configuration
db_config = {
    'user': 'root',          # Replace with your MySQL username
    'password':'',  # Replace with your MySQL password
    'host': 'localhost',
    'port':'3306',
    'database': 'ddos_detection'
}

# Function to get database connection
def get_db_connection():
    conn = mysql.connector.connect(**db_config)
    return conn

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('home'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']

        hashed_password = generate_password_hash(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, name, email, password, phone) VALUES (%s, %s, %s, %s, %s)",
                (username, name, email, hashed_password, phone)
            )
            conn.commit()
            flash('Registration successful! Please login.', 'success')
            return redirect(url_for('login'))
        except mysql.connector.IntegrityError:
            flash('Email already exists!', 'danger')
        finally:
            cursor.close()
            conn.close()

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            flash('Login successful!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password!', 'danger')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('login'))

@app.route('/home')
def home():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('home.html')

@app.route('/about')
def about():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('about.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file', 'danger')
            return redirect(request.url)
        if file and file.filename.endswith('.csv'):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)
            session['dataset_path'] = filepath
            df = pd.read_csv(filepath)
            data_html = df.head(10).to_html(classes='table table-striped', index=False)
            flash('File uploaded successfully!', 'success')
            return render_template('upload.html', data_html=data_html)
        else:
            flash('Invalid file type. Please upload a CSV file.', 'danger')

    return render_template('upload.html')
# Hardcoded accuracies for models (replace with actual values)
model_accuracies = {
    'Hybrid SVM-RF': 0.94,
    'Hybrid LR-KNN': 0.95,
    'Hybrid GB-XGB': 0.94,
}

@app.route('/algo')
def algo():
    # if 'email' not in session:
    #     return redirect(url_for('login'))
    try:
        return render_template('algo.html', accuracies=model_accuracies)
    except Exception as e:
        return f"Error rendering algo.html: {e}", 500


@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    selected_features = joblib.load('selected_features.pkl') if os.path.exists('selected_features.pkl') else []

    if request.method == 'POST':
        if not os.path.exists('model.pkl'):
            flash('Please train the model first in Algo page!', 'danger')
            return redirect(url_for('algo'))

        input_data = {}
        for feature in selected_features:
            try:
                input_data[feature] = float(request.form.get(feature, 0))
            except ValueError:
                flash(f'Invalid input for {feature}. Please enter a valid number.', 'danger')
                return redirect(url_for('predict'))

        df_input = pd.DataFrame([input_data])

        selector = joblib.load('selector.pkl')
        scaler = joblib.load('scaler.pkl')
        model = joblib.load('model.pkl')
        le = joblib.load('label_encoder.pkl')

        X_input_new = df_input[selected_features.values]
        X_input_scaled = scaler.transform(X_input_new)
        prediction = model.predict(X_input_scaled)
        result = le.inverse_transform(prediction)[0]

        return render_template('predict.html', result=result, features=selected_features)

    return render_template('predict.html', features=selected_features)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
