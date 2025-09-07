# Hotel Booking System - Django Backend

A comprehensive Django REST API backend for the Hotel Booking System with special date tracking, offers management, and spin wheel game functionality.

## 📁 Project Structure

This backend is located in the `backend/` folder of the main project:
```
backend/
├── hotel_backend/          # Django project settings
├── customer_management/    # Customer management app
├── events/                 # Events & special dates app
├── offers/                 # Offers management app
├── spin_wheel/            # Spin wheel game app
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
├── db.sqlite3            # SQLite database
└── README.md             # This file
```

## Features

### 🏨 Core Functionality
- **Customer Management**: Store and manage customer information
- **Special Dates Tracking**: Track birthdays, anniversaries, and other special dates
- **Events Management**: Manage hotel events and bookings
- **Offers System**: Create and manage promotional offers
- **Spin Wheel Game**: Customer engagement game with prizes

### 🔧 Technical Features
- Django REST Framework for API endpoints
- CORS support for Angular frontend integration
- SQLite database (easily configurable for production)
- Admin interface for data management
- Comprehensive API documentation
- Authentication and permissions

## Installation

1. **Navigate to Backend Directory**
   ```bash
   cd backend
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run Migrations**
   ```bash
   python manage.py migrate
   ```

4. **Create Superuser**
   ```bash
   python manage.py createsuperuser
   ```

5. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

## API Endpoints

### Customer Management (`/api/customers/`)
- `GET /api/customers/customers/` - List all customers
- `POST /api/customers/customers/` - Create new customer
- `GET /api/customers/customers/{id}/` - Get customer details
- `PUT /api/customers/customers/{id}/` - Update customer
- `DELETE /api/customers/customers/{id}/` - Delete customer
- `GET /api/customers/customers/search/?q=query` - Search customers
- `GET /api/customers/customers/{id}/special-dates/` - Get customer's special dates
- `GET /api/customers/customers/{id}/game-status/` - Check game play status

### Events (`/api/events/`)
- `GET /api/events/special-dates/` - List special dates
- `POST /api/events/special-dates/` - Create special date
- `GET /api/events/special-dates/upcoming/` - Get upcoming special dates
- `GET /api/events/special-dates/this-month/` - Get this month's special dates
- `GET /api/events/special-dates/stats/` - Get special dates statistics
- `GET /api/events/events/` - List events
- `POST /api/events/events/` - Create event
- `POST /api/events/events/{id}/book/` - Book an event
- `GET /api/events/bookings/` - List event bookings

### Offers (`/api/offers/`)
- `GET /api/offers/offers/` - List offers
- `POST /api/offers/offers/` - Create offer
- `GET /api/offers/offers/active/` - Get active offers
- `GET /api/offers/offers/expired/` - Get expired offers
- `POST /api/offers/offers/{id}/use/` - Use an offer
- `GET /api/offers/offers/stats/` - Get offer statistics
- `GET /api/offers/usages/` - List offer usages

### Spin Wheel (`/api/spin-wheel/`)
- `GET /api/spin-wheel/prizes/` - List prizes
- `POST /api/spin-wheel/prizes/` - Create prize
- `GET /api/spin-wheel/prizes/active/` - Get active prizes
- `POST /api/spin-wheel/games/play/` - Play spin wheel game
- `PATCH /api/spin-wheel/games/{id}/claim/` - Claim prize
- `GET /api/spin-wheel/games/stats/` - Get game statistics
- `GET /api/spin-wheel/sessions/played-customers/` - Get played customers
- `GET /api/spin-wheel/sessions/available-customers/` - Get available customers

## Database Models

### Customer Management
- **Customer**: Basic customer information (name, email, phone, birth_date)
- **CustomerProfile**: Extended customer profile with preferences and VIP status

### Events
- **SpecialDate**: Customer special dates (birthdays, anniversaries)
- **Event**: Hotel events and activities
- **EventBooking**: Event bookings by customers

### Offers
- **Offer**: Promotional offers with validity periods
- **OfferUsage**: Track offer usage by customers

### Spin Wheel
- **Prize**: Available prizes with probability settings
- **SpinWheelGame**: Game sessions and results
- **GameSession**: Track customer game participation (one-time play restriction)

## Admin Interface

Access the Django admin interface at `http://localhost:8000/admin/` to:
- Manage customers and their profiles
- View and edit special dates
- Manage events and bookings
- Create and monitor offers
- Configure spin wheel prizes
- View game statistics

## Configuration

### CORS Settings
The backend is configured to allow requests from:
- `http://localhost:4200` (Angular development server)
- `http://127.0.0.1:4200`

### Authentication
- Session authentication for web interface
- Token authentication for API access
- All API endpoints require authentication

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
```

### Database Reset
```bash
python manage.py flush
```

### Testing API
```bash
python test_api.py
```

## Production Deployment

For production deployment:
1. Set `DEBUG = False` in settings
2. Configure proper database (PostgreSQL recommended)
3. Set up static file serving
4. Configure CORS for production domains
5. Use environment variables for sensitive settings

## Integration with Angular Frontend

The backend is designed to work seamlessly with the Angular frontend:
- All API endpoints return JSON data
- CORS is configured for frontend communication
- Authentication tokens can be used for API access
- Real-time data synchronization through REST API

## License

This project is part of the Hotel Booking System.
