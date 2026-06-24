Easy Money Flow - Django Edition
Quick Start Guide (10 Minutes)

---

STEP-BY-STEP SETUP

1. DOWNLOAD AND EXTRACT

Extract the easy-money-flow-django folder to your desired location.

2. CREATE VIRTUAL ENVIRONMENT

cd easy-money-flow-django

# On macOS/Linux:
python -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
venv\Scripts\activate

3. INSTALL DEPENDENCIES

pip install -r requirements.txt

Wait for installation to complete. This installs Django, REST Framework, and M-Pesa integration tools.

4. INITIALIZE DATABASE

python manage.py makemigrations
python manage.py migrate

5. CREATE ADMIN ACCOUNT

python manage.py createsuperuser

Enter:
- Username: admin
- Email: admin@example.com
- Password: (your password)

6. COLLECT STATIC FILES

python manage.py collectstatic --noinput

7. START SERVER

python manage.py runserver

You should see:
Starting development server at http://127.0.0.1:8000/

---

ACCESSING YOUR APP

Open a web browser and visit:

Dashboard: http://localhost:8000/tracker/dashboard/
Admin: http://localhost:8000/admin/
Add Transaction: http://localhost:8000/tracker/add/
History: http://localhost:8000/tracker/history/
Analytics: http://localhost:8000/tracker/analytics/

---

FIRST TIME USAGE

1. LOGIN TO ADMIN

Visit http://localhost:8000/admin/
Use your superuser credentials

2. CREATE CATEGORIES

In admin, create transaction categories:
- Food & Dining
- Transport
- Utilities
- Entertainment
- Shopping
- Health & Medical
- Education
- Savings
- Investment
- Other

3. SET BUDGET

Go to Dashboard > Budget Settings
Enter your daily and monthly spending limits

4. ADD TRANSACTIONS

Click "Add Transaction"
Fill in amount, category, description, date
Click Save

5. VIEW ANALYTICS

Check spending patterns in Analytics section

---

DIRECTORY STRUCTURE

easy-money-flow-django/
├── manage.py                  # Django command utility
├── requirements.txt           # Python dependencies
├── .env.example              # Environment variables template
├── README.md                 # Full documentation
├── SETUP_GUIDE.md            # Detailed setup guide
├── QUICK_START.md            # This file
│
├── easy_money_flow/          # Project configuration
│   ├── __init__.py
│   ├── settings.py           # Django settings
│   ├── urls.py               # URL routing
│   ├── wsgi.py               # Production server
│   └── asgi.py               # Async server
│
├── tracker/                  # Main application
│   ├── models.py             # Database models
│   ├── views.py              # View logic
│   ├── forms.py              # HTML forms
│   ├── urls.py               # App URLs
│   ├── admin.py              # Admin configuration
│   │
│   ├── templates/
│   │   ├── base.html
│   │   └── tracker/
│   │       ├── dashboard.html
│   │       ├── add_transaction.html
│   │       ├── transaction_list.html
│   │       └── analytics.html
│   │
│   └── static/css/
│
├── api/                      # M-Pesa integration
│   ├── __init__.py
│   ├── mpesa_integration.py  # M-Pesa API client
│   ├── views.py              # API views
│   └── urls.py               # API URLs
│
├── templates/
├── static/
└── logs/

---

KEY FEATURES

Dashboard
- Real-time spending overview
- Budget progress bars
- Monthly income vs expense
- Category breakdown

Transactions
- Add expenses or income
- Categorize spending
- Filter by date, category, type
- View transaction history

Analytics
- 30-day spending trends
- Category analysis
- Top spending days
- Average daily spending

Budget Management
- Set daily limits
- Set monthly limits
- Choose currency
- Track against limits

M-Pesa Integration
- Receive transaction notifications
- Auto-import transactions
- Real-time updates
- Secure OAuth authentication

---

COMMON TASKS

Add a Transaction

1. Click "Add Transaction" in navigation
2. Enter amount
3. Select type (Expense or Income)
4. Choose category
5. Enter description (optional)
6. Select date and time
7. Click Save

View Transaction History

1. Click "History" in navigation
2. Use filters to narrow results
3. Filter by type, category, date range
4. Sort by date

Check Analytics

1. Click "Analytics" in navigation
2. View weekly breakdown
3. See category distribution
4. Find top spending days
5. Check insights

Update Budget

1. Click "Budget" in navigation
2. Enter daily limit
3. Enter monthly limit
4. Select currency
5. Click Save

---

TROUBLESHOOTING

Server won't start

Error: "Port 8000 already in use"
Solution: python manage.py runserver 8001

Error: "ModuleNotFoundError: No module named django"
Solution: Make sure virtual environment is activated
         pip install -r requirements.txt

Database errors

Error: "no such table: tracker_transaction"
Solution: python manage.py migrate

Error: "table already exists"
Solution: rm db.sqlite3
         python manage.py migrate

Template not found

Error: "TemplateDoesNotExist: base.html"
Solution: Check INSTALLED_APPS in settings.py
         Verify template directories exist
         python manage.py migrate

Static files not loading

Error: CSS/JS not displaying
Solution: python manage.py collectstatic --clear
         Restart server

---

ENVIRONMENT VARIABLES (.env)

Create .env file for configuration:

MPESA_CONSUMER_KEY=your_consumer_key
MPESA_CONSUMER_SECRET=your_consumer_secret
MPESA_ENVIRONMENT=sandbox
SECRET_KEY=your-secret-key

For production, set:
DEBUG=False
ALLOWED_HOSTS=yourdomain.com

---

SECURITY TIPS

Development
- Keep DEBUG=True (default)
- Use default SQLite database
- Secret key is for development only

Before Production
- Generate new SECRET_KEY
- Set DEBUG=False
- Use strong, random SECRET_KEY
- Configure ALLOWED_HOSTS
- Use HTTPS
- Use PostgreSQL instead of SQLite
- Store secrets in environment variables

---

M-PESA INTEGRATION (OPTIONAL)

Get Credentials

1. Visit https://developer.safaricom.co.ke
2. Create account and app
3. Copy Consumer Key and Consumer Secret

Configure

1. Copy .env.example to .env
2. Add your credentials
3. Update webhook URL in api/mpesa_integration.py

Test

python manage.py shell
from api.mpesa_integration import MPesaClient

client = MPesaClient('key', 'secret', 'sandbox')
response = client.initiate_stk_push('254700000000', 1000, 'USER', 'Test')
print(response)

---

NEXT STEPS

1. Explore the dashboard
2. Add test transactions
3. Check analytics
4. Read README.md for full features
5. Review SETUP_GUIDE.md for detailed information
6. Configure M-Pesa integration (optional)

---

HELPFUL COMMANDS

# Run development server
python manage.py runserver

# Open Django shell
python manage.py shell

# Create database backup
sqlite3 db.sqlite3 .dump > backup.sql

# View Django logs
tail -f logs/django.log

# Restart server (in another terminal)
python manage.py runserver 8001

# Clean up old migrations (careful!)
python manage.py makemigrations --empty tracker --name remove_unused

# See all registered URLs
python manage.py show_urls

---

GETTING HELP

If you encounter issues:

1. Check README.md
2. Read SETUP_GUIDE.md
3. Look at Django logs
4. Test in Django shell
5. Review error messages carefully

---

WHAT'S INCLUDED

Django Project Setup
- Complete project configuration
- Ready-to-use settings
- All apps configured
- Database models defined
- URL routing configured

Application Code
- Transaction tracking
- Budget management
- Analytics calculation
- M-Pesa integration
- Admin interface

Templates
- Base layout with M-Pesa styling
- Dashboard view
- Transaction form
- History view
- Analytics view

Database
- SQLite (lightweight, no setup needed)
- Pre-configured models
- Ready for data entry

Documentation
- This quick start guide
- Full README with features
- Detailed setup guide
- Code comments

---

YOU'RE READY!

You now have a complete financial tracking application. Start adding transactions and monitoring your spending!

For more information, see README.md and SETUP_GUIDE.md

Questions? Review the documentation or check Django docs at https://docs.djangoproject.com/

---

Version: 1.0.0
Last Updated: January 2024
License: MIT
