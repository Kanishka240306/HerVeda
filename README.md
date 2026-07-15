<div align="center">

# 🌸 HerVeda

![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-success?style=for-the-badge)

**A calm, mobile-friendly wellness app for tracking cycle health, wellbeing, and daily self-care.**

</div>

---

## 📌 About

HerVeda is a women’s wellness experience built to make cycle tracking and daily wellbeing support feel simple, gentle, and accessible. The app now includes a Flask-powered frontend with multiple pages for signup, login, dashboard, cycle tracking, assessments, and daily planning.

---

## ✨ What’s Included

- Responsive landing page with mobile-first design
- Signup and login forms that POST directly to Flask routes with data persistence
- Dashboard for daily wellbeing check-ins
- Cycle tracker for tracking symptoms, flow, and dates
- Wellbeing assessment form with energy and stress tracking
- Daily plan builder for creating personalized self-care routines
- Real data persistence: all form submissions saved to JSON files with timestamps
- Waitlist submission endpoint and health check endpoint
- Wine-themed color scheme optimized for mobile devices

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | HTML templates, CSS, JavaScript |
| Backend | Python, Flask |
| Data | JSON-based waitlist storage |
| Styling | Mobile-first responsive design |

---

## 📁 Project Structure

```text
HerVeda/
├── app.py                          # Flask backend with all route handlers
├── requirements.txt                # Python dependencies
├── waitlist.json                   # Email waitlist storage
├── data/
│   └── user_data.json              # Form submission data (signup, login, etc.)
├── static/
│   ├── css/
│   │   └── style.css               # Mobile-first responsive styling
│   └── js/
│       └── script.js               # Form UX enhancements
├── templates/
│   ├── base.html                   # Layout template with navbar & footer
│   ├── landing.html                # Welcome page with feature cards
│   ├── signup.html                 # User registration form
│   ├── login.html                  # User login form
│   ├── dashboard.html              # Daily wellbeing check-in
│   ├── cycle_tracker.html          # Cycle symptoms & flow tracker
│   ├── assessment.html             # Wellbeing assessment
│   └── daily_plan.html             # Daily self-care plan builder
├── .gitignore
└── README.md
```

---

## 🚀 How to Run Locally

1. Clone the repository
```bash
git clone https://github.com/Kanishka240306/HerVeda.git
cd HerVeda
```

2. Create and activate a virtual environment
```bash
python -m venv venv
venv\Scripts\activate      # Windows
# source venv/bin/activate # macOS/Linux
```

3. Install dependencies
```bash
pip install -r requirements.txt
```

4. Start the app
```bash
python app.py
```

Open http://localhost:3000 in your browser.

---

## 🌐 Main Routes

| Method | Route | Purpose |
|--------|-------|----------|
| GET | `/` | Landing page |
| GET/POST | `/signup` | User registration with data persistence |
| GET/POST | `/login` | User login form |
| GET/POST | `/dashboard` | Daily wellbeing check-in |
| GET/POST | `/cycle-tracker` | Cycle symptoms and flow tracking |
| GET/POST | `/assessment` | Wellbeing assessment form |
| GET/POST | `/daily-plan` | Daily self-care plan builder |
| POST | `/waitlist` | Email waitlist submission |
| GET | `/health` | Health check endpoint

---

## � How It Works

1. A user lands on the welcome page and explores the app's wellness tools.
2. They sign up or log in — form data is saved to `data/user_data.json` with a UTC timestamp.
3. They can track cycle symptoms/flow, complete wellbeing assessments, and create daily care plans.
4. Each form submits directly to Flask routes (POST), validates data, persists to JSON, then re-renders with confirmation feedback.
5. All user data is stored locally in JSON format with timestamps for each entry.

## 💾 Data Storage

Form submissions are automatically saved to `data/user_data.json` with the following structure:

```json
{
  "signup": [
    {"name": "...", "email": "...", "goal": "...", "createdAt": "ISO timestamp"},
    ...
  ],
  "login": [
    {"email": "...", "createdAt": "ISO timestamp"},
    ...
  ],
  "dashboard": [...],
  "cycle_tracker": [...],
  "assessment": [...],
  "daily_plan": [...]
}
```

Each entry includes a UTC `createdAt` timestamp for data tracking.

---


## 📸 Screenshots

| Login | Landing-home |
|-------|----------|
| ![Login](assessts/01-login.png) | ![Landing-home](assessts/02-landing-home.png) |

| Landing-home-scrolled | signup |
|-------------|--------------|
| ![Landing-home-scrolled](assessts/03-landing-home-scrolled.png) | ![signup](assessts/04-signup.png) |

| signup-scrolled | dashboard-checkin |
|--------------|---------------------|
| ![signup-scrolled](assessts/05-signup-scrolled.png) | ![dashboard-checkin](assessts/06-dashboard-checkin.png) |

| dashboard-checkin-scrolled | cycle -tracker |
|-----------------------|--------------------|
| ![dashboard-checkin-scrolled](assessts/07-dashboard-checkin-scrolled.png) | ![cycle-tracker](assessts/08-cycle-tracker.png) |

| cycle-tracker-scrolled | daily-plan |
|----------------------|-------------|
| ![cycle-tracker-scrolled](assessts/09-cycle-tracker-scrolled.png) | ![daily-plan](assessts/10-daily-plan.png)|

| daily-plan-scrolled | assessment |
|------------------|-------------|
| ![daily-plan-scrolled](assessts/11-daily-plan-scrolled.png) | ![assessment](assessts/12-assessment.png)|

| assessment-scrolled |
|-------------------|
| ![assessment-scrolled](assessts/13-assessment-scrolled.png)|


## �👥 Team

| Name | Role |
|------|------|
| Kanishka Sharma | Frontend & project lead |
| Anushka | Backend development |

---

## 📝 License

Proprietary — all rights reserved.