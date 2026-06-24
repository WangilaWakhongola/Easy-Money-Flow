Easy Money Flow - Django Edition

A modern personal finance tracker inspired by M-Pesa's design, built with Django and SQLite. Track daily spending, visualize budget flow, monitor money habits, and integrate with M-Pesa API for automatic transaction imports.

Django 4.2 | Python 3.8+ | SQLite | MIT License

---

FEATURES

Core Features
- Dashboard - Real-time overview of income, expenses, and budget status
- Daily Spending Tracker - Track today's spending with progress bar
- Monthly Budget Management - Set and monitor daily/monthly limits
- Transaction History - Filterable transaction log with search
- Category Tracking - Organize spending across 10+ categories
- Analytics & Insights - Detailed spending patterns and trends

Integration
- M-Pesa API Integration - Auto-import transactions via webhooks
- Transaction Notifications - Receive real-time M-Pesa updates
- Multi-currency Support - Track in KES, USD, EUR, GBP

Design
- M-Pesa Inspired UI - Signature green color scheme
- Mobile-First - Responsive design for all devices
- Modern Dashboard - Charts, heatmaps, and visualizations
- Dark Mode Ready - Easy to add dark theme

Security
- SQLite Database - Lightweight, file-based persistence
- User Authentication - Django built-in auth system
- CSRF Protection - Enabled by default
- Secure M-Pesa Integration - OAuth 2.0 authentication

---

PROJECT STRUCTURE

easy-money-flow-django/
├── manage.py                    # Django management script
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment variables template
├── db.sqlite3                   # SQLite database (created after setup)
│
├── easy_money_flow/            # Project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── tracker/                    # Main app
│   ├── migrations/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── urls.py
│   ├── admin.py
│   ├── apps.py
│   │
│   ├── templates/
│   │   ├── base.html
│   │   └── tracker/
│   │       ├── dashboard.html
│   │       ├── add_transaction.html
│   │       ├── transaction_list.html
│   │       └── analytics.html
│   │
│   └── static/
│       └── css/
│
├── api/                        # M-Pesa API handling
│   ├── __init__.py
│   ├── mpesa_integration.py
│   ├── views.py
│   └── urls.py
│
├── templates/
├── static/css/
└── logs/

---

QUICK START (5 MINUTES)

1. Prerequisites
- Python 3.8+
- pip
- Git

2. Clone & Setup

mkdir easy-money-flow
cd easy-money-flow

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate      # macOS/Linux
# or
venv\Scripts\activate         # Windows

3. Install Dependencies

pip install -r requirements.txt

4. Configure Django

The settings.py is already configured. Just update easy_money_flow/urls.py if needed.

5. Initialize Database

python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput

6. Run Server

python manage.py runserver

7. Access the app

- Dashboard: http://localhost:8000/tracker/dashboard/
- Admin: http://localhost:8000/admin/
- Add Transaction: http://localhost:8000/tracker/add/
- History: http://localhost:8000/tracker/history/
- Analytics: http://localhost:8000/tracker/analytics/

---

DATABASE MODELS

Transaction
{
    amount: Decimal
    transaction_type: 'expense' or 'income'
    category: ForeignKey(Category)
    description: str
    date: date
    time: time
    source: 'manual' or 'mpesa' or 'api' or 'bank'
    mpesa_transaction_id: str (unique)
}

Budget
{
    daily_limit: Decimal
    monthly_limit: Decimal
    currency: 'KES' or 'USD' or 'EUR' or 'GBP'
}

Category
{
    name: str
    icon: str
}

DailyLog
{
    date: date (unique)
    total_expense: Decimal
    total_income: Decimal
    transaction_count: int
    is_logged: bool
}

---

M-PESA API SETUP

1. Get Credentials
- Go to https://developer.safaricom.co.ke
- Register or login
- Create a new app
- Copy Consumer Key and Consumer Secret

2. Configure Environment
Create .env file:

MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_ENVIRONMENT=sandbox

3. Setup Webhook
Update the callback URL in api/mpesa_integration.py:

"CallBackURL": "https://yourdomain.com/api/mpesa/webhook/"

---

API ENDPOINTS

Dashboard
- GET /tracker/dashboard/ - Main dashboard

Transactions
- GET /tracker/add/ - Add transaction form
- POST /tracker/add/ - Save new transaction
- GET /tracker/history/ - Transaction history

Analytics
- GET /tracker/analytics/ - Analytics dashboard

Budget
- GET /tracker/budget/ - Budget settings form
- POST /tracker/budget/ - Update budget

M-Pesa Webhook
- POST /api/mpesa/webhook/ - Receive transaction notifications

---

SECURITY CHECKLIST

- Change SECRET_KEY (don't use development key)
- Set DEBUG = False in production
- Update ALLOWED_HOSTS with your domain
- Use HTTPS only
- Use environment variables for secrets
- Enable CSRF_COOKIE_SECURE
- Enable SESSION_COOKIE_SECURE
- Configure CORS properly
- Use strong password validators
- Enable rate limiting for API

---

DEPLOYMENT

Heroku

echo "web: gunicorn easy_money_flow.wsgi" > Procfile
echo "python-3.11.0" > runtime.txt

heroku login
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
heroku open

PythonAnywhere

1. Create account at pythonanywhere.com
2. Upload project
3. Create web app with Django
4. Configure static files
5. Reload

---

TROUBLESHOOTING

Database not found
python manage.py migrate

Static files not loading
python manage.py collectstatic --clear

M-Pesa API errors
- Check credentials in .env
- Verify callback URL is publicly accessible
- Check M-Pesa app status on developer portal

Template not found
- Ensure app is in INSTALLED_APPS in settings.py
- Check template path matches DIRS in settings

---

RESOURCES

- Django Documentation: https://docs.djangoproject.com/
- Django REST Framework: https://www.django-rest-framework.org/
- M-Pesa API Docs: https://developer.safaricom.co.ke/docs
- Python-Decouple: https://github.com/henriquebastos/python-decouple

---

CONTRIBUTING

1. Fork the repository
2. Create your feature branch (git checkout -b feature/AmazingFeature)
3. Commit your changes (git commit -m 'Add some AmazingFeature')
4. Push to the branch (git push origin feature/AmazingFeature)
5. Open a Pull Request

---

LICENSE

This project is licensed under the MIT License.

---

AUTHOR

Emmanuel Wangila Wakhongola
GitHub: https://github.com/WangilaWakhongola

---

Last Updated: January 2024
Version: 1.0.0
