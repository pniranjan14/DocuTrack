# DocuTrack – Academic Document Management Portal

## 📌 Overview
[cite_start]In many college departments, the process of collecting, storing, and verifying student academic documents (such as personal details, certificates, and reports) is largely manual and time-consuming[cite: 3]. [cite_start]This often results in an increased workload for faculty and administrative authorities[cite: 4]. 

[cite_start]**DocuTrack** is a department-specific web portal developed to solve this problem[cite: 5]. [cite_start]Built with Python Django as the backend framework, it streamlines academic document submission and verification by replacing generic cloud storage with a secure, centralized system[cite: 3, 5]. [cite_start]It offers a scalable, user-friendly solution that significantly reduces administrative burden and supports the transition toward a paperless academic environment[cite: 10].

## ✨ Key Features
* [cite_start]**Role-Based Access Control (RBAC):** Secure, separate login flows and dashboards for Students and Faculty members[cite: 6].
* [cite_start]**Student Portal:** Allows students to securely upload required departmental documents, update personal data, and track the real-time validation status of their files[cite: 7].
* [cite_start]**Faculty Console:** A centralized dashboard where teachers and administrative authorities can review, validate, and manage student submissions efficiently[cite: 7].
* [cite_start]**Secure File Handling:** Utilizes a structured database for efficient data storage, fast retrieval, and secure file handling mechanisms[cite: 8].
* [cite_start]**Automated Workflows:** Minimizes manual verification errors, improving overall efficiency, accuracy, and transparency in departmental academic management[cite: 9].

## 🛠️ Tech Stack
* **Frontend:** HTML5, CSS3, JavaScript (Custom Glassmorphism & Dark Mode UI)
* [cite_start]**Backend:** Python, Django [cite: 5]
* [cite_start]**Database:** SQLite / PostgreSQL (Structured for efficient data storage and retrieval) [cite: 8]
* **Architecture:** MVT (Model-View-Template)

## 📂 Frontend Architecture
The user interface is designed with a modern, enterprise-grade aesthetic and includes the following core views:
* `index.html` - Landing page with system overview
* `login.html` & `register.html` - Dynamic authentication modules
* `student_dashboard.html` & `student_profile.html` - Student workspaces
* `document_upload.html` - Secure file drop-zone
* `faculty_dashboard.html` & `verification_detail.html` - Verification and management consoles

## 🚀 Installation & Setup
*(Provide step-by-step instructions for anyone cloning your repo)*

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/pniranjan14/DocuTrack.git](https://github.com/pniranjan14/DocuTrack.git)
   cd DocuTrack
   ```

   ## 👨‍💻 Created By

   **P Niranjan**

   - 🌐 [Portfolio](https://niranjan-portfolio-gold.vercel.app/)
   - 🐙 [GitHub](https://github.com/pniranjan14)
   - 💼 [LinkedIn](https://www.linkedin.com/in/pniranjannn/)
