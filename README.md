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

- Responsive landing page
- Signup and login forms that POST directly to Flask routes
- Dashboard for daily wellbeing check-ins
- Cycle tracker for symptoms and flow
- Wellbeing assessment form
- Daily plan builder for self-care routines
- Waitlist submission endpoint and health check endpoint

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
├── app.py
├── requirements.txt
├── waitlist.json
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── script.js
├── templates/
│   ├── base.html
│   ├── landing.html
│   ├── signup.html
│   ├── login.html
│   ├── dashboard.html
│   ├── cycle_tracker.html
│   ├── assessment.html
│   └── daily_plan.html
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

- GET / → landing page
- GET/POST /signup → signup form
- GET/POST /login → login form
- GET/POST /dashboard → dashboard check-in
- GET/POST /cycle-tracker → cycle tracker entry
- GET/POST /assessment → wellbeing assessment
- GET/POST /daily-plan → daily plan form
- POST /waitlist → waitlist submission
- GET /health → health check

---

## 👥 Team

| Name | Role |
|------|------|
| Kanishka Sharma | Frontend & project lead |
| Anushka | Backend development |

---

## 📝 License

Proprietary — all rights reserved.