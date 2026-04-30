# 🔐 Break the Login – DASS Project

## 📌 Description

This project is a web application developed using Flask that demonstrates common security vulnerabilities and how they can be fixed.

The application includes both a vulnerable version and a secure version, allowing comparison between insecure and secure implementations.

---

## 🎯 Objectives

- Implement a basic authentication system
- Demonstrate common web vulnerabilities
- Exploit these vulnerabilities
- Apply security fixes
- Compare vulnerable vs secure behavior

---

## ⚙️ Technologies Used

- Python (Flask)
- SQLite
- HTML / CSS
- bcrypt (password hashing)

---

## 🚨 Vulnerabilities Implemented

The vulnerable version includes:

- Plain text password storage
- User Enumeration
- Brute Force attack
- SQL Injection
- IDOR (Insecure Direct Object Reference)
- Weak password reset tokens

---

## 🛠️ Security Fixes

The secure version includes:

- Password hashing using bcrypt
- Protection against brute force attacks
- Unified error messages (no user enumeration)
- Parameterized SQL queries (SQL Injection prevention)
- Access control for user data (IDOR fix)
- Secure random reset tokens
- Audit logging of user actions

---

## ▶️ How to Run

### 1. Clone repository

### 2. Create virtual environment

python3 -m venv venv  
source venv/bin/activate  

---

### 3. Install dependencies

pip install flask bcrypt  

---

### 4. Run vulnerable version

python app_vulner.py  

---

### 5. Run secure version

python app_secure.py  

---

## 🧪 Attack Demonstration

To simulate brute force attack:

python attack.py  

---

## 📊 Features

- User registration and login
- Note management (basic CRUD)
- Search functionality
- Password reset system
- Audit logging

---

## 🔍 Project Structure

- app_secure.py  
- vuln.py  
- attack.py  
- templates/  
- database.db  
- README.md  

---

## 🎓 Learning Outcomes

This project helped me understand:

- How web vulnerabilities work  
- How attackers exploit systems  
- How to secure applications properly  
- Importance of authentication and input validation  
- Role of logging in security monitoring  

---

## 📌 Conclusion

The project demonstrates the transition from a vulnerable system to a secure one by applying best practices in web security.

