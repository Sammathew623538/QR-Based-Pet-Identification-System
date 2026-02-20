# 🐾 PetQR - Smart Pet Identification System

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg) ![Django](https://img.shields.io/badge/Django-5.0-green.svg) ![Status](https://img.shields.io/badge/Status-Active-success.svg)

**PetQR** is a comprehensive web application designed to safeguard pets using **dynamic QR code technology** and **IoT concepts**. It serves as a digital bridge between lost pets and their owners, offering real-time tracking, instant profile access, and emergency alerts.

---

## 🚀 Key Features

### 🛡️ For Pet Owners
- **Dynamic QR Profiles:** Each pet gets a unique QR code. When scanned, it instantly shows a public profile with contact details and critical medical info.
- **🚨 Panic Button / Lost Mode:** Activate "Lost Mode" to instantly alert the community.
- **📄 Smart Poster Generation:** One-click generation of a "Missing Pet" poster (PDF) with the pet's photo and QR code (Powered by `ReportLab`).
- **🏥 Medical Records:** Store and manage vaccination history and medical needs.

### 🛒 Tag Ordering & Invoicing
- **Order Tags:** Integrated system to order physical QR tags/collars.
- **Invoice Generation:** Automatic PDF invoice generation for every order.
- **Order Tracking:** Track order status (Shipped, Delivered, Cancelled).

### 👮 Staff Dashboard
- **User Management:** Admins can view, edit, or delete users.
- **Order Management:** Process orders and update statuses efficiently.

---

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | **Django 5.0** (Python) | Robust and scalable web framework |
| **Database** | **SQLite** (Dev) | Relational database management |
| **Frontend** | **HTML5, CSS3, Bootstrap 5** | Responsive, mobile-first design |
| **QR Generation** | **qrcode & Pillow** | Dynamic QR code generation with embedded images |
| **PDF Tools** | **ReportLab** | Programmatic PDF creation for posters & invoices |

---

## ⚙️ Installation Guide

Follow these steps to run the project locally:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/Sammathew623538/-QR-Based-Pet-Identification-System-.git
   cd -QR-Based-Pet-Identification-System-
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start Server**
   ```bash
   python manage.py runserver
   ```
   Visit `http://127.0.0.1:8000/` in your browser.

---

## 🤝 Contribution

Contributions are welcome! Feel free to open issues or submit pull requests to improve the project.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
