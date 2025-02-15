from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pandas as pd
from openpyxl import load_workbook, Workbook
from models import db, Student  # Ensure correct import

app = Flask(__name__)
app.secret_key = "your_secret_key"

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Ensure Excel file exists
EXCEL_FILE = 'students_record.xlsx'
if not os.path.exists(EXCEL_FILE):
    wb = Workbook()
    ws = wb.active
    ws.append(["Student ID", "Name", "Age", "Status"])
    wb.save(EXCEL_FILE)

def update_excel():
    students = Student.query.all()
    data = [[s.student_id, s.name, s.age, "Active"] for s in students]
    df = pd.DataFrame(data, columns=["Student ID", "Name", "Age", "Status"])
    df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)

# Student model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)

# Create tables
with app.app_context():
    db.create_all()

# Home route
@app.route('/')
def home():
    return redirect(url_for('login'))

# Register route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        role = request.form.get('role', 'user')  # Default to user

        if User.query.filter_by(username=username).first():
            return render_template('register.html', error="Username already exists")

        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        new_user = User(username=username, password=hashed_password, role=role)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')

# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            return redirect(url_for('dashboard'))

        return render_template('login.html', error="Invalid credentials")

    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# Dashboard route
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        student_id = request.form['student_id']
        name = request.form['name']
        age = request.form['age']
        new_student = Student(student_id=student_id, name=name, age=int(age))
        db.session.add(new_student)
        db.session.commit()
        update_excel()

    students = Student.query.all()
    return render_template('dashboard.html', students=students, role=session.get('role'))

# File Upload Route
@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part', 'danger')
        return redirect(url_for('dashboard'))

    file = request.files['file']

    if file.filename == '':
        flash('No selected file', 'danger')
        return redirect(url_for('dashboard'))

    if file:
        try:
            df = pd.read_excel(file, engine='openpyxl')
        except Exception as e:
            flash(f"Error reading Excel file: {str(e)}", "danger")
            return redirect(url_for('dashboard'))

        df = df.dropna(how='all')
        expected_columns = {'student id', 'name', 'age'}
        df.columns = df.columns.str.strip().str.lower()
        if not expected_columns.issubset(df.columns):
            flash('Invalid Excel format. Ensure columns: "Student ID", "Name", "Age".', 'danger')
            return redirect(url_for('dashboard'))

        for _, row in df.iterrows():
            new_student = Student(
                student_id=int(row['student id']),  
                name=row['name'].strip(),
                age=int(row['age'])
            )
            db.session.add(new_student)
        db.session.commit()
        update_excel()
        flash('Students uploaded successfully!', 'success')
    return redirect(url_for('dashboard'))

# Delete Student (Admin only)
@app.route('/delete/<int:id>', methods=['POST'])
def delete_student(id):
    if session.get('role') != 'admin':
        flash("Permission denied", "danger")
        return redirect(url_for('dashboard'))

    student = Student.query.get(id)
    if student:
        df = pd.read_excel(EXCEL_FILE, engine='openpyxl')
        df.loc[df['Student ID'] == student.student_id, 'Status'] = 'Deleted'
        df.to_excel(EXCEL_FILE, index=False, engine='openpyxl')
        db.session.delete(student)
        db.session.commit()
        flash("Student deleted", "success")
    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)
