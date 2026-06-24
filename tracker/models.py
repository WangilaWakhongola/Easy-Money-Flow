from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator

class Budget(models.Model):
    """User's daily and monthly budget settings"""
    CURRENCY_CHOICES = [
        ('KES', 'Kenyan Shilling'),
        ('USD', 'US Dollar'),
        ('EUR', 'Euro'),
        ('GBP', 'British Pound'),
    ]
    
    daily_limit = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        default=5000,
        validators=[MinValueValidator(0)]
    )
    monthly_limit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=150000,
        validators=[MinValueValidator(0)]
    )
    currency = models.CharField(
        max_length=3,
        choices=CURRENCY_CHOICES,
        default='KES'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name_plural = "Budgets"
    
    def __str__(self):
        return f"Daily: {self.daily_limit} {self.currency}"


class Category(models.Model):
    """Transaction categories"""
    CATEGORY_CHOICES = [
        ('food', 'Food & Dining'),
        ('transport', 'Transport'),
        ('utilities', 'Utilities'),
        ('entertainment', 'Entertainment'),
        ('shopping', 'Shopping'),
        ('health', 'Health & Medical'),
        ('education', 'Education'),
        ('savings', 'Savings'),
        ('investment', 'Investment'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    icon = models.CharField(max_length=20, default='money')
    
    class Meta:
        verbose_name_plural = "Categories"
    
    def __str__(self):
        return self.get_name_display()


class Transaction(models.Model):
    """Individual spending transactions"""
    TRANSACTION_TYPE = [
        ('expense', 'Expense'),
        ('income', 'Income'),
    ]
    
    SOURCE_CHOICES = [
        ('manual', 'Manual Entry'),
        ('mpesa', 'M-Pesa SMS'),
        ('api', 'M-Pesa API'),
        ('bank', 'Bank Transfer'),
        ('card', 'Card'),
    ]
    
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )
    transaction_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_TYPE,
        default='expense'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    description = models.CharField(max_length=255, blank=True)
    date = models.DateField(default=timezone.now)
    time = models.TimeField(default=timezone.now)
    source = models.CharField(
        max_length=20,
        choices=SOURCE_CHOICES,
        default='manual'
    )
    mpesa_transaction_id = models.CharField(
        max_length=100,
        blank=True,
        unique=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-time']
        indexes = [
            models.Index(fields=['-date']),
            models.Index(fields=['date', 'transaction_type']),
        ]
    
    def __str__(self):
        return f"{self.transaction_type.upper()} - {self.amount} on {self.date}"
    
    @property
    def is_over_daily_limit(self):
        """Check if today's spending exceeds daily limit"""
        budget = Budget.objects.first()
        if not budget:
            return False
        
        today_expenses = Transaction.objects.filter(
            date=self.date,
            transaction_type='expense'
        ).aggregate(models.Sum('amount'))['amount__sum'] or 0
        
        return today_expenses > budget.daily_limit


class DailyLog(models.Model):
    """Aggregated daily spending data for performance"""
    date = models.DateField(unique=True, db_index=True)
    total_expense = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    total_income = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )
    transaction_count = models.IntegerField(default=0)
    is_logged = models.BooleanField(default=False)  # For logging streak
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date']
        verbose_name_plural = "Daily Logs"
    
    def __str__(self):
        return f"{self.date} - Exp: {self.total_expense}, Inc: {self.total_income}"
    
    @property
    def net = models.DecimalField(compute=True):
        return self.total_income - self.total_expense
