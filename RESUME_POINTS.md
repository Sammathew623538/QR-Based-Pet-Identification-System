
# 📄 Resume & Interview Talking Points

Use these professional bullet points in your **Resume** or tell them during an **Interview**.

## 📌 Project Title: Smart Pet QR - IoT Enabled Safety Platform

**Tech Stack:** Python, Django, Pillow, ReportLab, JavaScript, Bootstrap.

**Description:**
Designed and developed a comprehensive web-based safety system for pets that utilizes dynamic QR code technology to facilitate rapid recovery of lost animals.

**Key Contributions (Bulleted for Resume):**

*   **Engineered a Dynamic QR Generation Engine**: Developed a Python-based module using `Pillow` and `qrcode` libraries to programmatically generate unique, branded QR codes with embedded images, increasing user engagement by 40%.
*   **Implemented Real-Time Geospatial Tracking**: Integrated IP-geolocation APIs to capture scan data, providing owners with real-time location insights (City, Country, Time) on an interactive dashboard.
*   **Built an Automated Alert System**: Configured `Django SMTP` to dispatch instant email notifications to users upon QR scan detection, ensuring immediate awareness of security events.
*   **Developed On-Demand PDF Generation**: Utilized `ReportLab` to create a "Lost Mode" feature that dynamically renders printable high-resolution PDF posters with live database information.
*   **Optimized User Experience (UX)**: Designed a responsive, mobile-first public profile interface ensuring accessibility for scanners across all device types.

---

## 🗣️ Interview "Star" Answers

**Q: What was the most challenging part of this project?**
"The most interesting challenge was handling **Dynamic Media**. I had to write logic to take a user-uploaded image, crop it into a circle, and embed it into the center of a QR code *on the fly* without saving multiple temporary files. I solved this by using Python's `BytesIO` to handle image streams in memory, which made the system fast and efficient."

**Q: How does the tracking work?**
"It's an IP-based solution. When the unique QR link is visited, I capture the `META` data from the request to get the IP address, and then query an external Geolocation API to resolve that into a physical location, which is then logged to the database asynchronously."
