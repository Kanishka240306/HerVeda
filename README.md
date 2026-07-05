🌸 HerVeda — PCOS & Period Tracking for Women in India

<p align="center">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"/>
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white"/>
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"/>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/>
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge"/>
</p>
<p align="center">
  <b>A women's health app built for Indian women — tackling PCOS with regional diet plans, symptom tracking, and multilingual support.</b>
</p>

💡 Why HerVeda?

Over 10 crore Indian women are affected by PCOS, yet most period tracking apps are designed for Western users — no regional diet plans, no Hindi/Tamil support, no understanding of Indian lifestyle.

HerVeda is built differently. It is made in India, for India.


✨ Features

✅ Currently Built


🏠 Landing Page — Responsive design with waitlist signup (HTML5 + CSS3 + Vanilla JS)
📧 Email Waitlist System — Real-time validation, DNS domain verification, duplicate prevention
🩺 PCOS Symptom Tracker — Log daily symptoms, pain severity, period flow, mood, and notes
🖥️ Python/Flask Backend — REST API with /waitlist and /health endpoints, JSON data storage
📱 Fully Responsive — Works on mobile, tablet, and desktop


🔜 Coming Soon


📅 Period cycle tracking & predictions
🥗 Personalized North & South Indian diet plans for PCOS
🤖 AI assistant chatbot for PCOS guidance
👩‍⚕️ Doctor booking & teleconsultation
🌐 Multilingual support (Hindi, Tamil)
👥 Anonymous community forum
🔐 User accounts (Firebase Authentication)
🗄️ Firestore database (replacing JSON file storage)



🛠️ Tech Stack

LayerTechnologyFrontendHTML5, CSS3, Vanilla JavaScript (ES6)BackendPython 3 with FlaskData StorageJSON file (waitlist.json) — migrating to FirestoreFontsCormorant Garamond, Outfit (Google Fonts)HostingLocal dev — deployment coming soon


📁 Project Structure

HerVeda/
├── index.html              # Landing page + waitlist
├── symptom-tracker.html    # PCOS symptom tracker
├── style.css               # Global styles
├── script.js               # Frontend JS
├── app.py                  # Python/Flask backend
├── requirements.txt        # Python dependencies
├── waitlist.json           # Email waitlist data
└── README.md


🚀 Getting Started

Prerequisites


Python 3.9+
Git


Run Locally

bashgit clone https://github.com/Kanishka240306/HerVeda.git
cd HerVeda

# create and activate a virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux

# install dependencies
pip install -r requirements.txt

# run the server
python app.py

Open http://localhost:3000 in your browser.


🎨 Design System

TokenValuePrimary (Wine)#5c2430Accent (Amber)#c9924aSoft (Rose-gold)#c4898fBackground#faf6f2Display FontCormorant GaramondBody FontOutfit


📊 API Endpoints

POST /waitlist

json{ "email": "user@example.com" }

Returns 200 on success, 409 if email exists, 400 for invalid input.

GET /health

json{ "status": "ok", "service": "Herveda backend" }


👤 About the Team

Built by Kanishka Sharma — B.Tech Data Science student at MIET, AKTU University.
Published researcher | Women's health advocate | Builder

🔗 LinkedIn

Anushka — Backend Developer (Python/Flask)


📝 License

Proprietary — All rights reserved © Kanishka Sharma