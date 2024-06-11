from flask import request, jsonify, render_template, redirect, url_for, flash, session
from app import app
import pandas as pd
import sqlite3
import os
import uuid

# Secret key for session management
app.secret_key = 'supersecretkey'  # Replace with your own secret key

# Absolute path to the database file
db_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'your_database.db')
article_table = '文章数据库'
verification_code = 'YOUR_VERIFICATION_CODE'  # Set your verification code here

# Test credentials
test_credentials = {
    'testuser': 'password123'
}


# Function to load the DataFrame
def load_dataframe(table_name):
    conn = sqlite3.connect(db_file)
    df = pd.read_sql_query(f"SELECT * FROM {table_name}", conn)
    conn.close()
    return df


# Function to save the DataFrame
def save_dataframe(df, table_name):
    conn = sqlite3.connect(db_file)
    df.to_sql(table_name, conn, if_exists='replace', index=False)
    conn.close()


# Home route - Welcome screen
@app.route('/')
def welcome():
    return render_template('welcome.html')


# Start practice route
@app.route('/start_practice')
def start_practice():
    return render_template('login.html')


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in test_credentials and test_credentials[username] == password:
            session['username'] = username
            return redirect(url_for('landing'))
        else:
            flash('Invalid username or password', 'danger')
            return redirect(url_for('login'))
    return render_template('login.html')


# Landing page route
@app.route('/landing')
def landing():
    if 'username' not in session:
        return redirect(url_for('login'))
    df = load_dataframe(article_table)
    rows = df.to_dict(orient='records')
    return render_template('landing.html', rows=rows)


# Logout route
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('welcome'))


# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.form.to_dict()
        if data['verification_code'] != verification_code:
            flash('Invalid verification code', 'danger')
            return redirect(url_for('register'))

        # Generate a unique ID for 学员编号
        unique_id = str(uuid.uuid4())
        data['学员编号'] = unique_id
        data['姓名'] = data.pop('username')
        data['试用期验证码'] = data.pop('password')

        # Remove confirm_password and verification_code from data
        data.pop('confirm_password')
        data.pop('verification_code')

        df = load_dataframe(article_table)
        df = df.append(data, ignore_index=True)
        save_dataframe(df, article_table)
        return redirect(url_for('login'))
    return render_template('register.html')


# Add a new student (form)
@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    if request.method == 'POST':
        data = request.form.to_dict()
        df = load_dataframe(article_table)
        df = df.append(data, ignore_index=True)
        save_dataframe(df, article_table)
        return redirect(url_for('get_students'))
    return render_template('add_student.html')


# Get all students (view)
@app.route('/get_students')
def get_students():
    df = load_dataframe(article_table)
    students = df.to_dict(orient='records')
    return render_template('get_students.html', students=students)


# Get a specific student by student_id
@app.route('/students/<student_id>', methods=['GET'])
def get_student(student_id):
    df = load_dataframe(article_table)
    student = df[df['学员编号'] == student_id].to_dict(orient='records')
    if student:
        return jsonify(student[0])
    else:
        return jsonify({'error': 'Student not found'}), 404


# Update a student by student_id
@app.route('/students/<student_id>', methods=['PUT'])
def update_student(student_id):
    data = request.get_json()
    df = load_dataframe(article_table)
    index = df[df['学员编号'] == student_id].index
    if not index.empty:
        for key, value in data.items():
            df.at[index[0], key] = value
        save_dataframe(df, article_table)
        return jsonify({'message': 'Student updated successfully!'})
    else:
        return jsonify({'error': 'Student not found'}), 404


# Delete a student by student_id
@app.route('/students/<student_id>', methods=['DELETE'])
def delete_student(student_id):
    df = load_dataframe(article_table)
    index = df[df['学员编号'] == student_id].index
    if not index.empty:
        df = df.drop(index)
        save_dataframe(df, article_table)
        return jsonify({'message': 'Student deleted successfully!'})
    else:
        return jsonify({'error': 'Student not found'}), 404
