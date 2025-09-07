# Hotel Booking System

A comprehensive hotel booking system with special date tracking, offers management, and customer engagement features.

## 🏗️ Project Structure

```
hotel/
├── frontend/                 # Angular Frontend
│   └── hotel-booking/       # Angular application
├── backend/                 # Django Backend
│   ├── hotel_backend/       # Django project settings
│   ├── customer_management/ # Customer management app
│   ├── events/             # Events & special dates app
│   ├── offers/             # Offers management app
│   ├── spin_wheel/         # Spin wheel game app
│   ├── manage.py           # Django management script
│   ├── requirements.txt    # Python dependencies
│   ├── db.sqlite3         # SQLite database
│   └── README.md          # Backend documentation
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites
- Node.js (v16 or higher)
- Python (v3.8 or higher)
- Angular CLI
- pip (Python package manager)

### Frontend Setup (Angular)
```bash
cd frontend/hotel-booking
npm install
ng serve
```
Frontend will be available at: `http://localhost:4200`

### Backend Setup (Django)
```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```
Backend will be available at: `http://localhost:8000`

## 🎯 Features

### Frontend (Angular)
- **Dashboard**: Overview of hotel operations
- **Events Management**: Track customer special dates (birthdays, anniversaries)
- **Offers Management**: Create and manage promotional offers
- **Spin Wheel Game**: Customer engagement game with prizes
- **Authentication**: Secure login/logout system
- **Responsive Design**: Glassmorphism dark theme with mobile support

### Backend (Django REST API)
- **Customer Management**: Store and manage customer information
- **Special Dates Tracking**: Track birthdays, anniversaries, and other special dates
- **Events Management**: Manage hotel events and bookings
- **Offers System**: Create and manage promotional offers with usage tracking
- **Spin Wheel Game**: Customer engagement game with one-time play restriction
- **Admin Interface**: Complete admin panel for data management

## 🔧 Technology Stack

### Frontend
- **Angular 18**: Modern web framework
- **SCSS**: Advanced CSS with variables and mixins
- **Glassmorphism Design**: Modern UI with dark theme
- **Responsive Layout**: Mobile-first design approach

### Backend
- **Django 5.0**: Python web framework
- **Django REST Framework**: API development
- **SQLite**: Database (easily configurable for production)
- **CORS**: Cross-origin resource sharing for frontend integration

## 📊 API Endpoints

### Customer Management
- `GET /api/customers/customers/` - List all customers
- `POST /api/customers/customers/` - Create new customer
- `GET /api/customers/customers/{id}/` - Get customer details
- `GET /api/customers/customers/search/?q=query` - Search customers

### Events & Special Dates
- `GET /api/events/special-dates/` - List special dates
- `POST /api/events/special-dates/` - Create special date
- `GET /api/events/special-dates/upcoming/` - Get upcoming special dates
- `GET /api/events/events/` - List events
- `POST /api/events/events/{id}/book/` - Book an event

### Offers Management
- `GET /api/offers/offers/` - List offers
- `POST /api/offers/offers/` - Create offer
- `GET /api/offers/offers/active/` - Get active offers
- `POST /api/offers/offers/{id}/use/` - Use an offer

### Spin Wheel Game
- `GET /api/spin-wheel/prizes/` - List prizes
- `POST /api/spin-wheel/games/play/` - Play spin wheel game
- `PATCH /api/spin-wheel/games/{id}/claim/` - Claim prize
- `GET /api/spin-wheel/sessions/available-customers/` - Get available customers

## 🎨 Design Features

### Glassmorphism Theme
- **Transparent Cards**: Backdrop blur effects
- **Dark Theme**: Modern dark color scheme
- **Gradient Accents**: Beautiful color gradients
- **Smooth Animations**: Hover effects and transitions
- **Responsive Grid**: Adaptive layout for all screen sizes

### User Experience
- **Intuitive Navigation**: Easy-to-use interface
- **Real-time Updates**: Live data synchronization
- **Form Validation**: Client and server-side validation
- **Error Handling**: User-friendly error messages
- **Loading States**: Visual feedback for async operations

## 🔐 Security Features

- **Authentication**: Secure login system
- **Authorization**: Role-based access control
- **CORS Protection**: Configured for specific origins
- **Input Validation**: Server-side data validation
- **SQL Injection Protection**: Django ORM protection

## 📱 Mobile Support

- **Responsive Design**: Works on all device sizes
- **Touch-Friendly**: Optimized for mobile interactions
- **Progressive Web App**: PWA capabilities
- **Offline Support**: Service worker implementation

## 🚀 Deployment

### Frontend Deployment
```bash
cd frontend/hotel-booking
ng build --prod
# Deploy dist/ folder to your web server
```

### Backend Deployment
```bash
cd backend
# Configure production database (PostgreSQL recommended)
# Set DEBUG = False in settings
# Configure static file serving
# Deploy to your server
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is part of the Hotel Booking System.

## 🆘 Support

For support and questions:
- Check the documentation in each folder
- Review the API endpoints
- Test with the provided test scripts

---

**Happy Coding! 🎉**