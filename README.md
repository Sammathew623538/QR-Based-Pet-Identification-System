# 🐾 Smart Pet QR - Advanced Pet Identification & Safety System

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg) ![Django](https://img.shields.io/badge/Django-5.0-green.svg) ![Status](https://img.shields.io/badge/Status-Active-success.svg)

## 🚀 Project Overview
**Smart Pet QR** is a full-stack web application designed to modernize pet safety. It combines **IoT concepts** with **Web Engineering** to create a seamless system where every pet gets a digital identity. The system allows owners to manage their pets, track scans in real-time, order physical tags, and generate emergency posters instantly.

---

## 🌟 Full Feature List

### 👤 1. User Authentication & Profile Management
- **Secure Sign-Up/Login**: Robust authentication system using Django's built-in auth.
- **Profile Management**: Users can update their personal details, address, and phone number.
- **Account Deactivation**: Option for users to securely deactivate and delete their account and data.

### 🐾 2. Pet Management & Safety Protocol
- **Add & Manage Pets**: easy interface to add multiple pets with photos, breed, age, and medical notes.
- **Dynamic QR Code Generation**:
  - Automatically generates a unique QR code for every pet.
  - **Custom Branding**: Embeds the pet's photo into the center of the QR code using `Pillow`.
  - **Downloadable**: Users can download the QR code PNG to print on labels or tags.
- **Public Pet Profile**:
  - A privacy-focused public page accessible via scanning the QR code.
  - Displays Owner's Contact, Emergency Number, and Medical Conditions (e.g., "Diabetic").
  - **"Scan to Call"**: One-tap calling button for finder.

### 📍 3. Real-Time Tracking & Emergency Alerts
- **Smart Scan Tracking**:
  - Records the **IP Address**, **Timestamp**, and **Approximate Location (City, Country)** of the scanner.
  - Displays scan history on the owner's dashboard.
- **🚨 Panic Mode ("Lost Mode")**:
  - One-click toggle to mark a pet as "Lost".
  - **Instant Email Alert**: Sends an immediate email notification to the owner when the QR is scanned.
- **📄 Smart Poster Generator**:
  - Automatically generates a high-quality **PDF Missing Poster**.
  - Includes Pet Photo, Name, Reward Details, and QR Code.
  - Uses `ReportLab` for pixel-perfect PDF creation.

### 🏥 4. Medical Records System
- **Digital Health Book**: Store vaccination dates, vet visits, and medical history.
- **Critical Info Display**: Highlights life-saving information (allergies, medications) on the public profile.

### 🛍️ 5. E-Commerce Module (Tag Ordering)
- **Shop Premium Tags**: Users can order NFC/QR collars directly from the dashboard.
- **Order Management**:
  - **Place Order**: Select design, add shipping address, and confirm.
  - **Order Tracking**: Visual stepper tracking (Pending -> Packed -> Shipped -> Delivered).
  - **Cancellation**: Users can cancel orders before they are shipped.
- **🧾 Auto-Invoice Generation**:
  - Generates a professional PDF Invoice for every confirmed order.
  - Downloadable directly from the Order Details page.
- **Product Reviews**:
  - Verified buyers can rate and review collars (Star Rating + Comments).
  - Public review display on the product page.

### 🤖 6. AI-Assisted Support Chatbot
- **Integrated Smart Bot**: A JavaScript-based chatbot on the Order Details page.
- **Context-Aware**:
  - Instantly answers questions like *"Where is my order?"* or *"Can I cancel?"*.
  - Fetches real-time status of the specific order being viewed.

### 👮 7. Staff & Admin Dashboard
- **Dedicated Staff Portal**: Restricted area for admins and staff.
- **Stats Overview**: View total Users, Pets, and Scans today.
- **User Management**: Staff can view, edit, or delete user accounts.
- **Order Processing**: Staff can update order statuses (e.g., mark as "Shipped").

---

## 🛠️ Technical Stack & Libraries

| Category | Technology Used | Purpose |
| :--- | :--- | :--- |
| **Backend Framework** | **Django 5.0 (Python)** | Core logic, routing, and database ORM |
| **Database** | **SQLite** (Dev) | Lightweight relational database |
| **Frontend** | **HTML5, CSS3, Bootstrap 5** | Responsive, mobile-first UI |
| **Image Processing** | **Pillow (PIL)** | generating QR codes with embedded images |
| **PDF Engine** | **ReportLab** | Generating Missing Posters and Invoices |
| **Geolocation** | **Requests & ip-api** | converting Scanner IP to physical location |
| **Email Service** | **Django SMTP** | Sending security alerts |
| **Scripting** | **JavaScript (ES6)** | Chatbot logic and dynamic UI interactions |

---

## ⚙️ Installation Guide

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
