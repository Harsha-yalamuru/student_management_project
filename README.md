# student_management_project
Student Management System A Flask-based web application for managing student data. This project allows users to view student details (name, age) and add new students dynamically(manually and also upload excel format files). Built with Python, Flask, HTML, CSS, this application demonstrates basic CRUD (Create, Read, Update, Delete) operations.
# Student Database Management System (Flask-Based)

## 📌 Project Overview
This **Student Database Management System** is a **Flask-based web application** that allows **admins** and **users (students)** to manage student records. The system supports **manual data entry, Excel file uploads, and automatic record keeping in an Excel file** while maintaining role-based access control.

---

## 🎯 Features
### **1️⃣ Authentication System**
- **User Registration & Login**
- Passwords are securely stored using **hashing**
- **Session-based authentication**
- **Role-based access control**
  - **Admin**: Can add, upload, and delete students.
  - **User (Student)**: Can only add and view student records.

### **2️⃣ Student Record Management**
- **Add new students manually via UI**
- **Upload bulk student records using Excel (.xlsx)**
- **Display all student records in a table**
- **Admins can delete student records**

### **3️⃣ Excel Integration**
- **All records (manually added and uploaded) are stored in a new Excel file (`students_record.xlsx`).**
- **Deleted students are not permanently erased but marked as "Deleted" in the Excel file.**

### **4️⃣ Database**
- Uses **SQLite** as the database.
- Stores **users and students**.

---

## 🏗️ Project Structure
📂 admission_management
│── 📂 static
│   └── styles.css             # CSS for frontend styling
│── 📂 templates
│   ├── dashboard.html         # Main UI for student management
│   ├── login.html             # Login page
│   ├── register.html          # Registration page
│── 📜 models.py               # Database models (User, Student)
│── 📜 main.py                 # Main Flask app
│── 📜 students_record.xlsx    # Excel file storing student details
│── 📜 requirements.txt        # Dependencies list
│── 📜 README.md               # Project documentation
---
## 📝 Usage

### 1️⃣ Register & Login(Role Assigned Into USER OR ADMIN For ACCESS To Differing Features).
- Open [http://127.0.0.1:5000/register](http://127.0.0.1:5000/register) to create an account.  
- Default role is `user`. Set **role to 'admin'** in the database for admin access.
---
![Screenshot (571)](https://github.com/user-attachments/assets/85100d3b-510d-4d8c-a79b-ff10b6dcd290)
![Screenshot (564)](https://github.com/user-attachments/assets/5075f215-c015-44ef-8c4c-704776277eb2)
![Screenshot (565)](https://github.com/user-attachments/assets/0c266041-f7b4-4836-af17-629b98966e80)
## Dashboard
---
![Screenshot (566)](https://github.com/user-attachments/assets/81bdb57e-dd08-4f2d-a988-dbaf110d703f)

### 2️⃣ Add Students(Dynamically Add Data Manually And Also Via Datasets)
- Enter **Name, Student ID, Age** manually.  
- Upload an **Excel file** (EXCEL format - .xslv)containing student details.
---
![Screenshot (567)](https://github.com/user-attachments/assets/a32c040f-cf6c-45fe-ba2a-f656c6aac589)

### 3️⃣ Delete Students (Admin Only), Deletion Of Single or Multiple Records.
![Screenshot (568)](https://github.com/user-attachments/assets/4d586cc2-3de8-4a0a-898d-bde6098d59ba)
- **Only admins** can delete student records.  
- **Deleted students** will be logged in `students_record.xlsx`.
## Addition Of Student Details.
---
![Screenshot (569)](https://github.com/user-attachments/assets/864f2856-59c1-4961-9a0e-66bcce21b7c7)
### 4️⃣ Edit Each Field or Column in Data Manually if Required.
---
![Screenshot (573)](https://github.com/user-attachments/assets/91cdf184-9023-4a9b-9046-eb60362796a0)
![Screenshot (575)](https://github.com/user-attachments/assets/4c9339d7-9d3d-418d-bbac-4d5bde284045)

## Backend Visibility Of Student Records Saved With Their Status Informing Whether They are Deleted Records (Listed).
---
![Screenshot (570)](https://github.com/user-attachments/assets/80f9798a-3522-4161-b453-2e31a8587e4f)
![Screenshot (574)](https://github.com/user-attachments/assets/27876e4c-2843-4b03-b732-5240c9b0d237)

