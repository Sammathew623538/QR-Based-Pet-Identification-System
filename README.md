# QR-Based-Pet-Identification-System




# 🐾 QR-Based Pet Identification & Rescue System

A Django-based web application that helps pet owners protect and track their pets using QR code-enabled smart identification collars.

This system allows anyone who finds a lost pet to scan the QR code on the pet’s collar and instantly access essential information such as the owner’s contact details, medical records, and emergency instructions — helping reunite lost pets with their families faster.

---

## 🚀 Features

### 👤 User Module

* User Registration & Login Authentication
* Profile Management
* Add / Update / Delete Pets
* Upload Pet Images
* Activate Lost Mode for Pets
* Download QR Code for Pet Identification

---

### 📱 QR Scan Tracking

* Public pet profile accessible via QR scan
* Automatic scan history recording
* Real-time owner notification system via Email
* Emergency contact display

---

### 🐕 Pet Management

* Add pet details (Name, Breed, Age, Gender, Color)
* Emergency contact information
* Upload medical records
* Toggle Lost Mode
* Download pet QR Code

---

### 📊 Dashboard

* View all registered pets
* Track scan activity
* Monitor lost pets
* View recent scan history
* Order smart pet collars

---

### 🛒 Smart Collar Order System

* Place QR-enabled collar orders
* Order tracking
* Invoice generation
* Cancel orders
* Submit product reviews

---

### 🧑‍💼 Staff Admin Panel

* View total users
* Manage pet records
* Monitor scan history
* View orders
* Edit or delete users

---

### 🧾 Lost Pet Poster Generator

* Automatically generate printable PDF poster
* Includes:

  * Pet Image
  * Owner Contact
  * Pet Details
  * Reward Badge
  * Embedded QR Code

---

### 📍 Location Tracking

* Displays scan history to pet owner

---

## 🛠️ Tech Stack

| Technology | Usage                 |
| ---------- | --------------------- |
| Python     | Backend Logic         |
| Django     | Web Framework         |
| SQLite     | Database              |
| HTML       | Frontend              |
| CSS        | Styling               |
| JavaScript | UI Interaction        |
| Pillow     | Image Processing      |
| ReportLab  | PDF Poster Generation | |

---

## ⚙️ Installation Guide

### 1️⃣ Clone Repository

```bash
git clone https://github.com/your-username/QR-Based-Pet-Identification-System.git
```

### 2️⃣ Navigate to Project Folder

```bash
cd QR-Based-Pet-Identification-System
```

### 3️⃣ Create Virtual Environment

```bash
python -m venv env
env\Scripts\activate
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 5️⃣ Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 6️⃣ Run Server

```bash
python manage.py runserver
```

---

## 📌 How It Works

1. Pet owner registers and adds pet details.
2. System generates a unique QR Code for each pet.
3. QR Code is attached to the pet’s smart collar.
4. If the pet is lost, anyone can scan the QR code.
5. Pet owner receives scan alert with location details.
6. Owner can download a missing poster instantly.

---



## 📧 Email Notification

Owner receives an automatic email alert when their pet’s QR code is scanned.

---

## 📄 License

This project is developed for educational and research purposes.

---

## 👨‍💻 Developed By

**Sam Mathew**
Python Full Stack Developer
Techmindz
