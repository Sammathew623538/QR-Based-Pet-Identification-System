# 🐾 Smart Pet QR - Next Gen Pet Safety System

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg) ![Django](https://img.shields.io/badge/Django-5.0-green.svg) ![Status](https://img.shields.io/badge/Status-Active-success.svg)

## 🚀 Overview
**Smart Pet QR** is an innovative web application engineered to bridge the gap between physical pet tags and digital identity using **IoT concepts**. Unlike traditional tags, this system generates **dynamic, trackable QR codes** that offer real-time data, location insights, and medical history access.

Built with **Django**, this project demonstrates advanced backend logic including **Dynamic Image Processing**, **Real-time Geolocation**, and **SMTP Email Notifications**.

---

## 🌟 Key Features

### 1. 🛡️ Intelligent QR Code Generation
- **Automated Design**: Upon registration, the system automatically generates a unique QR code using `Python` & `Pillow`.
- **Custom Branding**: The pet’s profile photo is cropped into a circular format and embedded directly into the center of the high-redundancy QR code.

### 2. 📍 Smart Scan Tracking & Alerts
- **Real-Time Geolocation**: Records the **Timestamp** and **Approximate Location (City/Country)** based on the scanner's IP address.
- **📩 Email Notifications**: Uses **Django SMTP** to instantly email the owner when their pet is scanned, providing immediate awareness.
- **Owner Dashboard**: Owners can view a history of all scan attempts to track their pet's last known location.

### 3. 🚨 "Lost Mode" Protocol
- **One-Click Activation**: Pet owners can toggle "Lost Mode" instantly from their dashboard.
- **Auto-Generated Assets**: The system uses `ReportLab` to instantly generate a printable, high-resolution **PDF Missing Poster** pre-filled with the pet's photo, contact details, and QR code.

### 4. 🏥 Comprehensive Medical Profile & Secure Auth
- **Medical Info**: Public profile displays critical medical conditions (e.g., "Needs Insulin") and vet contact info.
- **Secure Authentication**: Robust user profile management with secure login/logout and password handling.

### 5. 🛒 Integrated E-Commerce & Staff Dashboard
- **Order System**: A specialized module for ordering physical NFC/QR tags.
- **Admin/Staff Control**: Role-based access control for managing users and pets.

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | **Django 5.0** (Python) | Robust, scalable web framework |
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
