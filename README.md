# 🐾 Smart Pet QR - Advanced Pet Identification & Safety System

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg) ![Django](https://img.shields.io/badge/Django-5.0-green.svg) ![Status](https://img.shields.io/badge/Status-Active-success.svg)

## 🚀 Overview
**Smart Pet QR** is a full-stack web application designed to modernize pet safety. It combines **IoT concepts** with **Web Engineering** to create a seamless system where every pet gets a digital identity. The system allows owners to manage their pets, track scans in real-time, **book premium smart collars**, and generate emergency posters instantly.

---

## 🌟 Full Feature List

### 🛒 1. Smart Collar Booking & E-Commerce Store (New!)
- **Shop Premium Collars**: Integrated store where users can browse and book physical Smart QR Collars.
- **Design Selection**: Users can choose from multiple editions like **Classic, Sporty, Luxury, and Glow**.
- **Seamless Booking Flow**:
  - Select Pet -> Choose Design -> Enter Shipping Address -> Place Order.
  - Supports **Cash on Delivery** or Online Payment flows.
- **Order Tracking System**:
  - Visual timeline tracking: **Ordered ➝ Packed ➝ Shipped ➝ Delivered**.
  - Users can cancel orders if they change their mind before shipping.
- **Auto-Invoicing**: Automatically generates and lets users download a **PDF Invoice** for every collar booking.

### 🛡️ 2. Intelligent QR Code Generation
- **Automated Design**: Upon registration, the system automatically generates a unique QR code using `Python` & `Pillow`.
- **Custom Branding**: The pet’s profile photo is cropped into a circular format and embedded directly into the center of the high-redundancy QR code.

### 📍 3. Smart Scan Tracking & Alerts
- **Real-Time Geolocation**: Records the **IP Address**, **Timestamp**, and **Approximate Location** of the scanner.
- **📩 Email Notifications**: Uses **Django SMTP** to instantly email the owner when their pet is scanned.
- **Owner Dashboard**: Owners can view a history of all scan attempts to track their pet's last known location.

### 🤖 4. AI-Assisted Support Chatbot
- **Instant Order Help**: A built-in JavaScript chatbot on the Order Details page.
- **Smart Responses**: Capable of answering queries about **Order Status**, **Delivery Estimates**, and **Cancellation Policies** dynamically based on the specific order's state.

### 🚨 5. "Lost Mode" Protocol
- **One-Click Activation**: Pet owners can toggle "Lost Mode" instantly.
- **Auto-Generated Assets**: The system uses `ReportLab` to generate a printable **PDF Missing Poster** pre-filled with the pet's photo, contact details, and QR code.

### 🏥 6. Comprehensive Medical Profile
- **Medical Info**: Public profile displays critical medical conditions (e.g., "Needs Insulin") and vet contact info.
- **Secure Authentication**: Robust user profile management with secure login/logout.

### 👮 7. Staff & Admin Dashboard
- **User Management**: Admins can view, edit, or delete users.
- **Order Management**: Staff can process collar orders, update delivery status, and handle cancellations.

---

## 🛠️ Technical Stack

| Category | Technology Used | Purpose |
| :--- | :--- | :--- |
| **Backend** | **Django 5.0 (Python)** | Core logic, routing, and database ORM |
| **E-Commerce** | **Custom Django Models** | Order processing, Reviews, and Invoicing |
| **Database** | **SQLite** (Dev) | Lightweight relational database |
| **Frontend** | **HTML5, CSS3, Bootstrap 5** | Responsive, mobile-first UI |
| **Image Processing** | **Pillow (PIL)** | Generating QR codes with embedded images |
| **PDF Engine** | **ReportLab** | Generating Missing Posters and Invoices |
| **Geolocation** | **Requests & ip-api** | Converting Scanner IP to physical location |
| **Email Service** | **Django SMTP** | Sending security alerts |

---

## ⚙️ Installation & Setup

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
