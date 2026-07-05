<div align="center">

# 🌸 HerVeda — PCOS & Period Tracking for Women in India

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)
![License](https://img.shields.io/badge/License-Proprietary-blue?style=for-the-badge)

**A women's health app built for Indian women — tackling PCOS with regional diet plans, symptom tracking, and multilingual support.**

</div>

---

## 📌 About

Over 10 crore Indian women are affected by PCOS, yet most period tracking apps are designed for Western users — no regional diet plans, no Hindi/Tamil support, no understanding of Indian lifestyle. HerVeda is built differently: made in India, for India.

---

## ✨ Features

| Feature | Status |
|---------|--------|
| Landing Page (responsive) | ✅ Done |
| Email Waitlist System (DNS validation + duplicate prevention) | ✅ Done |
| PCOS Symptom Tracker (symptoms, flow, mood, notes) | ✅ Done |
| Python/Flask Backend (`/waitlist`, `/health`) | ✅ Done |
| Period cycle tracking & predictions | ⏳ Coming Soon |
| Personalized North & South Indian diet plans | ⏳ Coming Soon |
| Firebase Authentication (Email + Google) | ⏳ Coming Soon |
| Firestore database (replacing JSON storage) | ⏳ Coming Soon |
| AI assistant chatbot for PCOS guidance | ⏳ Coming Soon |
| Doctor booking & teleconsultation | ⏳ Coming Soon |
| Multilingual support (Hindi, Tamil) | ⏳ Coming Soon |
| Anonymous community forum | ⏳ Coming Soon |

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, Vanilla JavaScript |
| Backend | Python 3, Flask |
| Database | JSON file (`waitlist.json`) — migrating to Firestore |
| Fonts | Cormorant Garamond, Outfit (Google Fonts) |
| Hosting | Local dev — deployment coming soon |

---

## 📁 Project Structure

```
HerVeda/
├── index.html              ← Landing page + waitlist
├── symptom-tracker.html    ← PCOS symptom tracker
├── style.css                ← Global styles
├── script.js                ← Frontend JS
├── app.py                   ← Main backend (Flask)
├── requirements.txt         ← Python dependencies
├── waitlist.json            ← Email waitlist data
├── .gitignore
└── README.md
```

---

## 🚀 How to Run

**1. Clone the repository**
```bash
git clone https://github.com/Kanishka240306/HerVeda.git
cd HerVeda
```

**2. Create and activate a virtual environment**
```bash
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # macOS/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Run the app**
```bash
python app.py
```

Open `http://localhost:3000` in your browser.

---

## 🎨 Design System

| Token | Value |
|-------|-------|
| Primary (Wine) | `#5c2430` |
| Accent (Amber) | `#c9924a` |
| Soft (Rose-gold) | `#c4898f` |
| Background | `#faf6f2` |
| Display Font | Cormorant Garamond |
| Body Font | Outfit |

---

## 📊 API Endpoints

**`POST /waitlist`**
```json
{ "email": "user@example.com" }
```
Returns `200` on success, `409` if email exists, `400` for invalid input.

**`GET /health`**
```json
{ "status": "ok", "service": "Herveda backend" }
```

---

## 👥 Team

| Name | Role |
|------|------|
| **Kanishka Sharma** — [LinkedIn](https://www.linkedin.com/in/kanishka-sharma-623b53335/) | Frontend & Project Lead |
| **Anushka** — [LinkedIn](https://www.linkedin.com/in/anushka-773aa5337/) | Backend Developer (Python/Flask) |

---

## 📝 License

Proprietary — All rights reserved © Kanishka Sharma