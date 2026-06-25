# Herveda - PCOS & Period Tracking for Women in India

Herveda is an elegant, modern landing page and waitlist signup system for a PCOS and period tracking application designed specifically for women in India.

## 🌸 Features

- **Beautiful Landing Page**: Clean, responsive design with wine, amber, and rose-gold color scheme
- **Email Validation**: Real-time validation with DNS domain verification
- **Waitlist System**: Secure email collection with duplicate prevention
- **Modern Backend**: Built with Dart and Shelf framework
- **Responsive Design**: Works perfectly on mobile, tablet, and desktop

## 🛠️ Tech Stack

- **Frontend**: HTML5, CSS3, Vanilla JavaScript (ES6)
- **Backend**: Dart with Shelf web framework
- **Data Storage**: JSON file (waitlist.json)
- **Server**: Local development at http://localhost:3000

## 📋 Project Structure

```
HerVeda/
├── index.html          # Main landing page
├── style.css           # Complete styling
├── script.js           # Frontend interactivity
├── bin/
│   └── server.dart     # Dart backend server
├── pubspec.yaml        # Dart dependencies
├── .gitignore         # Git configuration
└── README.md          # This file
```

## 🚀 Getting Started

### Prerequisites
- Dart SDK (3.0.0 or higher)
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone git@github.com:Kanishka240306/HerVeda.git
   cd HerVeda
   ```

2. **Install Dart dependencies**
   ```bash
   dart pub get
   ```

3. **Run the server**
   ```bash
   dart run bin/server.dart
   ```

4. **Access the application**
   Open your browser and go to: `http://localhost:3000`

## 📧 API Endpoints

### POST /waitlist
Submit an email to the waitlist.

**Request:**
```json
{
  "email": "user@example.com"
}
```

**Response (Success):**
```json
{
  "success": true,
  "message": "Email added to waitlist"
}
```

**Response (Error):**
```json
{
  "success": false,
  "message": "Invalid email format" // or other error message
}
```

**Status Codes:**
- `200` - Email successfully added
- `400` - Invalid email format or validation failed
- `409` - Email already exists in waitlist

### GET /health
Health check endpoint.

**Response:**
```json
{
  "status": "ok",
  "service": "Herveda backend"
}
```

## ✨ Features in Detail

### Email Validation
- Format validation using regex
- DNS domain verification (ensures domain exists)
- Duplicate email prevention
- Timestamps stored in ISO 8601 format

### User Interface
- Smooth mobile menu toggle
- Loading states on form submission
- Success/error message display
- Responsive design for all screen sizes

## 📊 Data Storage

Emails are stored in `waitlist.json` with the following format:
```json
[
  {
    "email": "user@example.com",
    "createdAt": "2026-06-25T10:30:00.000Z"
  }
]
```

## 🎨 Design

- **Primary Color**: Wine (#5c2430)
- **Secondary Color**: Amber (#c9924a)
- **Accent Color**: Rose-gold (#c4898f)
- **Background**: Cream (#faf6f2)

**Typography:**
- Display: Cormorant Garamond
- Body: Outfit

## 🔐 Security

- Email validation prevents invalid data entry
- DNS verification ensures legitimate domains
- Duplicate prevention avoids spam
- Input sanitization on backend

## 📱 Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Mobile browsers (iOS Safari, Chrome Mobile)

## 📝 License

This project is currently proprietary. All rights reserved.

## 👤 Author

Created by Kanishka Sharma

## 📧 Contact

For questions or feedback, please reach out through the GitHub repository.

---

**Status**: The Herveda landing page and backend are fully functional and ready for deployment.
