# 🐾 Smart Pet QR - Next Gen Pet Safety System

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg) ![Django](https://img.shields.io/badge/Django-5.0-green.svg) ![Status](https://img.shields.io/badge/Status-Active-success.svg)

## 🚀 Overview
**Smart Pet QR** is an innovative web application engineered to bridge the gap between physical pet tags and digital identity using **IoT concepts**. Unlike traditional tags, this system generates **dynamic, trackable QR codes** that offer real-time data, location insights, and medical history access.

Built with **Django**, this project demonstrates advanced backend logic including **Dynamic Image Processing**, **Real-time Geolocation**, **AI-Assisted Support Chatbot**, and **SMTP Email Notifications**.

---

## 🔄 Project Workflow (How it Works)
1. **Registration & Pet Profile:** 
   - User signs up and adds their pet's details (Photo, Breed, Medical Info).
   - The system **automatically generates a unique QR code** with the pet's photo embedded in the center.

2. **Smart Scanning & Tracking:**
   - Anyone scanning the QR code gets redirected to the **Public Pet Profile**.
   - **Instant Alert:** The owner receives an **Email Notification** with the scanner's **IP Address** and **Approximate Location (City/Country)**.

3. **Emergency 'Lost Mode':**
   - If a pet goes missing, the owner toggles **"Lost Mode"** on their dashboard.
   - The system instantly generates a **High-Resolution Missing Poster (PDF)** ready for printing.

4. **E-Commerce & Support:**
   - Owners can order physical collars/tags directly.
   - **🤖 Smart Chatbot:** An integrated AI-like chatbot helps users track orders, check delivery status, and handle cancellations instantly.

---

## 🌟 Key Features

### 1. 🛡️ Intelligent QR Code Generation
- **Automated Design**: Upon registration, the system automatically generates a unique QR code using `Python` & `Pillow`.
- **Custom Branding**: The pet’s profile photo is cropped into a circular format and embedded directly into the center of the high-redundancy QR code.

### 2. 📍 Smart Scan Tracking & Alerts
- **Real-Time Geolocation**: Records the **Timestamp** and **Approximate Location** based on the scanner's IP address.
- **📩 Email Notifications**: Uses **Django SMTP** to instantly email the owner when their pet is scanned.
- **Owner Dashboard**: Owners can view a history of all scan attempts to track their pet's last known location.

### 3. 🤖 AI-Assisted Chatbot Support
- **Instant Order Help**: A built-in JavaScript chatbot on the order page assists users.
- **Smart Responses**: Capable of answering queries about **Order Status**, **Delivery Estimates**, and **Cancellation Policies** dynamically based on the specific order's state.

### 4. 🚨 "Lost Mode" Protocol
- **One-Click Activation**: Pet owners can toggle "Lost Mode" instantly.
- **Auto-Generated Assets**: The system uses `ReportLab` to generate a printable **PDF Missing Poster** pre-filled with the pet's photo, contact details, and QR code.

### 5. 🏥 Comprehensive Medical Profile
- **Medical Info**: Public profile displays critical medical conditions (e.g., "Needs Insulin") and vet contact info.
- **Secure Authentication**: Robust user profile management with secure login/logout.

### 6. 🛒 Integrated E-Commerce & Staff Dashboard
- **Order System**: A specialized module for ordering physical NFC/QR tags.
- **Invoice Generation**: Automatic PDF invoice generation for every order.
- **Staff Control**: Role-based access control for admins to manage users and pets.

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | **Django 5.0** (Python) | Robust, scalable web framework |
| **Chatbot** | **JavaScript (ES6)** | Frontend-based smart assistant |
| **Email** | **Django SMTP** | System for sending real-time alerts |
| **Database** | **SQLite** (Dev) | Relational data management |
| **Image Processing** | **Pillow (PIL)** | Dynamic image manipulation |
| **PDF Generation** | **ReportLab** | Programmatic PDF creation |
| **Geolocation** | **Requests & IP-API** | IP-to-Location conversion service |
| **Frontend** | **HTML5, CSS3, Bootstrap 5** | Responsive, mobile-first interface |

---

## 🔧 Installation & Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Sammathew623538/-QR-Based-Pet-Identification-System-.git
   cd -QR-Based-Pet-Identification-System-
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start the Server**
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` in your browser.

---

## 📄 License
This project is licensed under the MIT License.
