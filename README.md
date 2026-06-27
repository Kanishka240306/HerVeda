# 🌸 HerVeda — PCOS & Period Tracking for Women in India

<p align="center">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white"/>
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white"/>
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black"/>
  <img src="https://img.shields.io/badge/Dart-0175C2?style=for-the-badge&logo=dart&logoColor=white"/>
  <img src="https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge"/>
</p>

<p align="center">
  <b>A women's health app built for Indian women — tackling PCOS with regional diet plans, symptom tracking, and multilingual support.</b>
</p>

---

## 💡 Why HerVeda?

Over 10 crore Indian women are affected by PCOS, yet most period tracking apps are designed for Western users — no regional diet plans, no Hindi/Tamil support, no understanding of Indian lifestyle.

HerVeda is built differently. It is made in India, for India.

---

## ✨ Features

### ✅ Currently Built
- 🏠 **Landing Page** — Responsive design with waitlist signup (HTML5 + CSS3 + Vanilla JS)
- 📧 **Email Waitlist System** — Real-time validation, DNS domain verification, duplicate prevention
- 🩺 **PCOS Symptom Tracker** — Log daily symptoms, pain severity, period flow, mood, and notes
- 🖥️ **Dart/Shelf Backend** — REST API with `/waitlist` and `/health` endpoints, JSON data storage
- 📱 **Fully Responsive** — Works on mobile, tablet, and desktop

### 🔜 Coming Soon
- 📅 Period cycle tracking & predictions
- 🥗 Personalized North & South Indian diet plans for PCOS
- 🤖 AI assistant chatbot for PCOS guidance
- 👩‍⚕️ Doctor booking & teleconsultation
- 🌐 Multilingual support (Hindi, Tamil)
- 👥 Anonymous community forum

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML5, CSS3, Vanilla JavaScript (ES6) |
| Backend | Dart with Shelf framework |
| Data Storage | JSON file (waitlist.json) |
| Fonts | Cormorant Garamond, Outfit (Google Fonts) |
| Hosting | Local dev — deployment coming soon |

---

## 📁 Project Structure

```
HerVeda/
├── index.html              # Landing page + waitlist
├── symptom-tracker.html    # PCOS symptom tracker
├── style.css               # Global styles
├── script.js               # Frontend JS
├── server.js               # Node.js server (alt backend)
├── bin/
│   └── server.dart         # Dart/Shelf backend
├── pubspec.yaml            # Dart dependencies
├── waitlist.json           # Email waitlist data
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Dart SDK 3.0+
- Git

### Run Locally

```bash
git clone https://github.com/Kanishka240306/HerVeda.git
cd HerVeda
dart pub get
dart run bin/server.dart
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

### `POST /waitlist`
```json
{ "email": "user@example.com" }
```
Returns `200` on success, `409` if email exists, `400` for invalid input.

### `GET /health`
```json
{ "status": "ok", "service": "Herveda backend" }
```

---

## 👤 About the Developer

Built by **Kanishka Sharma** — B.Tech Data Science student at MIET, AKTU University.
Published researcher | Women's health advocate | Builder

🔗 [LinkedIn](https://www.linkedin.com/in/kanishka-sharma-623b53335)

---

## 📝 License

Proprietary — All rights reserved © Kanishka Sharma