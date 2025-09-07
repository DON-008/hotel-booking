# 🏨 Hotel Booking System

A modern, full-stack hotel booking and restaurant management system built with Angular and Django. This system is designed for hotels whose main business is restaurants, focusing on customer special dates tracking, offers management, and automated WhatsApp messaging.

## 🌟 Features

### 🎯 Core Functionality
- **Customer Management**: Store and manage customer information
- **Special Dates Tracking**: Track birthdays, anniversaries, and other special occasions
- **Offers Management**: Create and manage promotional offers
- **WhatsApp Integration**: Automated wish messages with special offers
- **Spin Wheel Game**: Interactive customer engagement tool
- **Dashboard**: Comprehensive overview of upcoming events and analytics

### 🎨 Modern UI/UX
- **Glassmorphism Design**: Modern, elegant dark theme
- **Responsive Layout**: Works perfectly on desktop, tablet, and mobile
- **Angular Material**: Professional component library
- **SCSS Styling**: Advanced CSS with custom animations

### 🔧 Technical Features
- **JWT Authentication**: Secure user authentication
- **RESTful API**: Django REST Framework backend
- **Real-time Updates**: Live data synchronization
- **Lazy Loading**: Optimized performance with lazy-loaded modules
- **PWA Ready**: Progressive Web App capabilities

## 🏗️ Project Structure

```
hotel/
├── backend/                 # Django Backend
│   ├── authentication/     # User authentication
│   ├── customer_management/ # Customer CRUD operations
│   ├── events/             # Special dates management
│   ├── offers/             # Offers management
│   ├── spin_wheel/         # Spin wheel game
│   ├── whatsapp/           # WhatsApp integration
│   └── hotel_backend/      # Django settings
├── hotel-booking/          # Angular Frontend
│   ├── src/app/components/ # Angular components
│   ├── src/app/services/   # API services
│   └── src/app/guards/     # Route guards
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Node.js (v18 or higher)
- Python (v3.11 or higher)
- Git

### Backend Setup (Django)

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Start development server:**
   ```bash
   python manage.py runserver
   ```

### Frontend Setup (Angular)

1. **Navigate to frontend directory:**
   ```bash
   cd hotel-booking
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start development server:**
   ```bash
   npm start
   ```

4. **Access the application:**
   - Frontend: http://localhost:4200
   - Backend API: http://localhost:8000/api
   - Django Admin: http://localhost:8000/admin

## 📱 Deployment

### Option 1: Netlify + Heroku (Recommended)

#### Frontend to Netlify:
1. Build the Angular app: `npm run build`
2. Drag & drop `dist/hotel-booking` folder to Netlify
3. Or connect GitHub repository for automatic deployments

#### Backend to Heroku:
1. Install Heroku CLI
2. Create Heroku app: `heroku create your-app-name`
3. Add PostgreSQL: `heroku addons:create heroku-postgresql:mini`
4. Deploy: `git push heroku main`
5. Run migrations: `heroku run python manage.py migrate`

### Option 2: Vercel + Railway
- Frontend: Deploy to Vercel
- Backend: Deploy to Railway

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
DEBUG=False
SECRET_KEY=your-secret-key
DATABASE_URL=your-database-url

# WhatsApp Configuration (Optional)
WHATSAPP_API_TOKEN=your-whatsapp-token
WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id
WHATSAPP_MOCK_MODE=True

# CORS Settings
CORS_ALLOW_ALL_ORIGINS=False
```

### API Configuration

Update the API URL in `hotel-booking/src/app/services/api.service.ts`:

```typescript
private baseUrl = 'https://your-backend-url.com/api';
```

## 📊 API Endpoints

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout

### Customers
- `GET /api/customers/` - List customers
- `POST /api/customers/` - Create customer
- `GET /api/customers/{id}/` - Get customer details
- `PUT /api/customers/{id}/` - Update customer
- `DELETE /api/customers/{id}/` - Delete customer

### Special Dates
- `GET /api/events/special-dates/` - List special dates
- `POST /api/events/special-dates/` - Create special date
- `PUT /api/events/special-dates/{id}/` - Update special date
- `DELETE /api/events/special-dates/{id}/` - Delete special date

### Offers
- `GET /api/offers/` - List offers
- `POST /api/offers/` - Create offer
- `PUT /api/offers/{id}/` - Update offer
- `DELETE /api/offers/{id}/` - Delete offer

### WhatsApp
- `POST /api/whatsapp/send-wish/` - Send wish message
- `POST /api/whatsapp/send-message/` - Send custom message

## 🎮 Usage Guide

### 1. Authentication
- Register a new account or login with existing credentials
- Access is required for all features except authentication

### 2. Dashboard
- View upcoming special dates
- Quick access to all features
- Analytics and statistics

### 3. Events Management
- Add new customers and their special dates
- Filter by date type (Birthday, Anniversary, etc.)
- Send automated wishes via WhatsApp or SMS

### 4. Offers Management
- Create promotional offers
- Set discount values and types
- Activate/deactivate offers
- Use offers in wish messages

### 5. Spin Wheel Game
- Interactive customer engagement
- One-time play per customer
- Collect customer data for marketing

## 🔒 Security Features

- JWT token-based authentication
- CORS protection
- Input validation and sanitization
- Secure password hashing
- Environment variable protection

## 🎨 Design System

### Color Palette
- Primary: Purple gradient (#a855f7 to #ec4899)
- Background: Dark glassmorphism
- Text: White with transparency
- Accents: Glass effects with blur

### Typography
- Modern, clean fonts
- Responsive sizing
- Gradient text effects
- Proper contrast ratios

## 🚀 Performance Optimizations

- Lazy loading for Angular modules
- OnPush change detection
- Optimized bundle sizes
- Efficient API pagination
- Caching strategies

## 🧪 Testing

### Backend Testing
```bash
cd backend
python manage.py test
```

### Frontend Testing
```bash
cd hotel-booking
npm test
```

## 📈 Future Enhancements

- [ ] Real-time notifications
- [ ] Advanced analytics dashboard
- [ ] Email marketing integration
- [ ] Multi-language support
- [ ] Mobile app development
- [ ] Advanced reporting features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation
- Review the API endpoints

## 🎯 Demo

Live demo available at: [Your deployed URL]

---

**Built with ❤️ using Angular and Django**