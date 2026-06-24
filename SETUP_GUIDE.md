Easy Money Flow - Django Version
Setup and Configuration Guide

A personal finance tracker inspired by M-Pesa's design, built with Django and SQLite.

---

FEATURES

Overview Dashboard - Income vs expenses, budget flow bars, spending allocation donut chart
Daily Spending Tracker - Set a daily limit, track today's spending with a live progress bar
Monthly Management - Track spending against monthly limits
Analytics Dashboard - 30-day trend, category breakdown, insights
Transaction Log - Full transaction history with filtering
M-Pesa Design - Built with M-Pesa's signature green palette and mobile-app feel
Persistent Storage - All data saved locally in SQLite database
M-Pesa API Integration - Auto-import transactions via webhooks

---

GETTING STARTED

This is a complete Django web app with no external dependencies beyond what's in requirements.txt.

1. PREREQUISITES

- Python 3.8 or higher
- pip (Python package manager)
- Virtual environment support (built-in to Python 3.3+)

2. CREATE VIRTUAL ENVIRONMENT

mkdir easy-money-flow
cd easy-money-flow

# Create virtual environment
python -m venv venv

# Activate it
On macOS/Linux:
source venv/bin/activate

On Windows:
venv\Scripts\activate

3. INSTALL DEPENDENCIES

pip install -r requirements.txt

This installs:
- Django 4.2.0 (web framework)
- Django REST Framework 3.14.0 (API)
- python-decouple 3.8 (environment variables)
- requests 2.31.0 (HTTP requests for M-Pesa)
- Pillow 10.0.0 (image handling)
- django-cors-headers 4.2.0 (CORS support)

4. DJANGO PROJECT SETUP

The project structure is already configured:

easy_money_flow/          - Project settings and configuration
tracker/                  - Main financial tracking app
api/                      - M-Pesa API integration
templates/                - Global HTML templates
static/                   - CSS, JavaScript, images
logs/                     - Application logs

5. DATABASE CONFIGURATION

The project uses SQLite by default (configured in settings.py).

Initialize the database:

python manage.py makemigrations
python manage.py migrate

Create an admin superuser:

python manage.py createsuperuser

Follow the prompts to create an admin account.

6. COLLECT STATIC FILES

python manage.py collectstatic --noinput

7. RUN DEVELOPMENT SERVER

python manage.py runserver

The server will start at http://localhost:8000

---

ACCESSING THE APPLICATION

After starting the server, access:

Dashboard
http://localhost:8000/tracker/dashboard/

Admin Interface
http://localhost:8000/admin/
(Use your superuser credentials)

Add Transaction
http://localhost:8000/tracker/add/

Transaction History
http://localhost:8000/tracker/history/

Analytics
http://localhost:8000/tracker/analytics/

Budget Settings
http://localhost:8000/tracker/budget/

---

M-PESA API INTEGRATION (OPTIONAL)

STEP 1: GET M-PESA CREDENTIALS

1. Go to https://developer.safaricom.co.ke
2. Sign up or log in
3. Create a new application
4. Copy the following:
   - Consumer Key
   - Consumer Secret
   - Business Shortcode (for STK Push)
   - Passkey (for encryption)

STEP 2: SET ENVIRONMENT VARIABLES

Create or edit .env file in your project root:

MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_ENVIRONMENT=sandbox
MPESA_BUSINESS_SHORTCODE=174379
MPESA_PASSKEY=bfb279f9aa9bdbcf158e97dd1a503017

STEP 3: UPDATE WEBHOOK URL

In api/mpesa_integration.py, update the callback URL:

"CallBackURL": "https://yourdomain.com/api/mpesa/webhook/"

Replace yourdomain.com with your actual domain when deploying.

STEP 4: TEST THE INTEGRATION

from api.mpesa_integration import MPesaClient

client = MPesaClient(
    consumer_key='your_key',
    consumer_secret='your_secret',
    environment='sandbox'
)

# Initiate payment
response = client.initiate_stk_push(
    phone_number='254700000000',
    amount=1000,
    account_ref='USER001',
    description='Test payment'
)
print(response)

---

TECH STACK

Backend
- Django 4.2 (Web framework)
- Django REST Framework (API)
- SQLite (Database)
- Python 3.8+ (Language)

Frontend
- HTML5 (Structure)
- CSS3 (Styling and animations)
- Vanilla JavaScript (Interactivity)

Integration
- M-Pesa API (Payment processing)
- OAuth 2.0 (Authentication)

---

KEY MODELS

Transaction Model
- amount (Decimal)
- transaction_type (expense or income)
- category (ForeignKey to Category)
- description (text)
- date (date)
- time (time)
- source (manual, mpesa, api, bank)
- mpesa_transaction_id (unique identifier)
- created_at, updated_at (timestamps)

Budget Model
- daily_limit (Decimal)
- monthly_limit (Decimal)
- currency (KES, USD, EUR, GBP)
- created_at, updated_at (timestamps)

Category Model
- name (food, transport, utilities, entertainment, shopping, health, education, savings, investment, other)
- icon (icon class or emoji)

DailyLog Model
- date (unique)
- total_expense (Decimal)
- total_income (Decimal)
- transaction_count (integer)
- is_logged (boolean)
- created_at, updated_at (timestamps)

---

VIEWS AND ENDPOINTS

DashboardView
GET /tracker/dashboard/
Shows overview of spending, budget status, and statistics

TransactionCreateView
GET /tracker/add/ - Display form
POST /tracker/add/ - Save transaction

TransactionListView
GET /tracker/history/ - Display history with filters
Supports filtering by type, category, date range

AnalyticsView
GET /tracker/analytics/ - Display analytics dashboard
Shows weekly breakdown, category analysis, top days

BudgetEditView
GET /tracker/budget/ - Display budget form
POST /tracker/budget/ - Update budget limits

MPesaWebhookView
POST /api/mpesa/webhook/ - Receive M-Pesa notifications
Auto-imports transactions from M-Pesa API

---

FORMS

TransactionForm
Fields: amount, transaction_type, category, description, date, time, source

BudgetForm
Fields: daily_limit, monthly_limit, currency

TransactionFilterForm
Fields: transaction_type, category, start_date, end_date, min_amount, max_amount

---

ADMIN INTERFACE

The Django admin interface is fully configured at /admin/

Manage:
- Transactions
- Budgets
- Categories
- Daily Logs

---

DEPLOYMENT

HEROKU DEPLOYMENT

1. Create Procfile:
echo "web: gunicorn easy_money_flow.wsgi" > Procfile

2. Create runtime.txt:
echo "python-3.11.0" > runtime.txt

3. Install Gunicorn:
pip install gunicorn

4. Update requirements.txt:
pip freeze > requirements.txt

5. Deploy:
heroku login
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
heroku open

PYTHONANYWHERE DEPLOYMENT

1. Create account at pythonanywhere.com
2. Upload project files
3. Create web app with Django as framework
4. Configure path to WSGI file
5. Set Python version to 3.11
6. Configure static files path
7. Reload web app

---

SECURITY CONFIGURATION

PRODUCTION SETTINGS

In settings.py, update:

DEBUG = False
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
SECRET_KEY = 'your-long-random-secret-key'

SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

DATABASE SECURITY

For production, use PostgreSQL instead of SQLite:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'easy_money_flow_db',
        'USER': 'postgres',
        'PASSWORD': 'secure_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

---

ENVIRONMENT VARIABLES

Essential variables in .env:

Django
SECRET_KEY=your-secret-key-here
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,yourdomain.com

M-Pesa
MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_ENVIRONMENT=sandbox

Database (if using PostgreSQL)
DATABASE_NAME=easy_money_flow_db
DATABASE_USER=postgres
DATABASE_PASSWORD=secure_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

---

TROUBLESHOOTING

No module named 'django'
Solution: pip install -r requirements.txt

Database errors
Solution: python manage.py migrate

Static files not loading
Solution: python manage.py collectstatic --clear

Port 8000 already in use
Solution: python manage.py runserver 8001

Template not found
Solution: Ensure INSTALLED_APPS includes your apps and DIRS is configured

---

LOGGING AND DEBUGGING

Enable Django shell for testing:

python manage.py shell

Query transactions:
from tracker.models import Transaction
transactions = Transaction.objects.all()

Check database:
python manage.py dbshell

View logs:
tail -f logs/django.log

---

FIRST TIME SETUP CHECKLIST

- Create virtual environment
- Install dependencies
- Run migrations
- Create superuser
- Collect static files
- Create budget limits
- Add transaction categories
- Add test transactions
- Test M-Pesa integration (if using)
- Configure production settings before deployment

---

COMMON COMMANDS

Create migrations for changes
python manage.py makemigrations

Apply migrations
python manage.py migrate

Create superuser
python manage.py createsuperuser

Run development server
python manage.py runserver

Collect static files
python manage.py collectstatic

Django shell (interactive Python)
python manage.py shell

Create new app
python manage.py startapp appname

Flush database (delete all data)
python manage.py flush

Make specific app migrations
python manage.py makemigrations tracker

---

RESOURCES

Django Official Docs: https://docs.djangoproject.com/
Django REST Framework: https://www.django-rest-framework.org/
M-Pesa API Documentation: https://developer.safaricom.co.ke/docs
Python-Decouple: https://github.com/henriquebastos/python-decouple
Gunicorn: https://gunicorn.org/
PostgreSQL: https://www.postgresql.org/

---

SUPPORT

For issues or questions:
1. Check the README.md file
2. Review Django documentation
3. Check application logs in logs/ directory
4. Test in Django shell
5. Review M-Pesa API documentation

---

Version: 1.0.0
Last Updated: January 2024
License: MIT
