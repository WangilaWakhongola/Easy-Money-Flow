from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count, Q
from django.utils import timezone
from django.http import JsonResponse
from datetime import timedelta, datetime
from decimal import Decimal
import json

from .models import Transaction, Budget, DailyLog, Category
from .forms import TransactionForm, BudgetForm


class DashboardView(LoginRequiredMixin, View):
    """Main dashboard showing overview, spending allocation, and trends"""
    
    def get(self, request):
        today = timezone.now().date()
        
        # Get or create budget
        budget = Budget.objects.first() or Budget.objects.create()
        
        # Today's spending
        today_transactions = Transaction.objects.filter(
            date=today,
            transaction_type='expense'
        )
        today_expense = today_transactions.aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
        
        # Month summary
        month_start = today.replace(day=1)
        month_transactions = Transaction.objects.filter(
            date__gte=month_start,
            date__lte=today
        )
        month_expense = month_transactions.filter(
            transaction_type='expense'
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
        month_income = month_transactions.filter(
            transaction_type='income'
        ).aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
        
        # Spending allocation by category
        category_spending = Transaction.objects.filter(
            date__gte=month_start,
            transaction_type='expense'
        ).values('category__name').annotate(
            total=Sum('amount')
        ).order_by('-total')
        
        # Last 30 days trend
        thirty_days_ago = today - timedelta(days=30)
        daily_logs = DailyLog.objects.filter(
            date__gte=thirty_days_ago,
            date__lte=today
        ).order_by('date')
        
        # Logging streak
        consecutive_logged = 0
        check_date = today
        while True:
            log = DailyLog.objects.filter(date=check_date, is_logged=True).exists()
            if log:
                consecutive_logged += 1
                check_date -= timedelta(days=1)
            else:
                break
        
        # Over limit warning
        is_over_daily = today_expense > budget.daily_limit
        
        context = {
            'budget': budget,
            'today_expense': today_expense,
            'daily_limit': budget.daily_limit,
            'daily_remaining': max(budget.daily_limit - today_expense, Decimal('0')),
            'daily_progress_percent': min((today_expense / budget.daily_limit * 100) if budget.daily_limit > 0 else 0, 100),
            'is_over_daily': is_over_daily,
            
            'month_expense': month_expense,
            'month_income': month_income,
            'month_net': month_income - month_expense,
            'month_progress_percent': min((month_expense / budget.monthly_limit * 100) if budget.monthly_limit > 0 else 0, 100),
            
            'category_spending': list(category_spending),
            'transaction_count_today': today_transactions.count(),
            'consecutive_logged_days': consecutive_logged,
            'daily_logs_30': list(daily_logs.values('date', 'total_expense')),
        }
        
        return render(request, 'tracker/dashboard.html', context)


class TransactionCreateView(LoginRequiredMixin, CreateView):
    """Add a new transaction"""
    model = Transaction
    form_class = TransactionForm
    template_name = 'tracker/add_transaction.html'
    success_url = '/tracker/dashboard/'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['budget'] = Budget.objects.first()
        return context


class TransactionListView(LoginRequiredMixin, ListView):
    """View transaction history with filtering"""
    model = Transaction
    template_name = 'tracker/transaction_list.html'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Transaction.objects.all()
        
        # Filter by transaction type
        trans_type = self.request.GET.get('type')
        if trans_type in ['expense', 'income']:
            queryset = queryset.filter(transaction_type=trans_type)
        
        # Filter by category
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category__name=category)
        
        # Filter by date range
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        if start_date:
            queryset = queryset.filter(date__gte=start_date)
        if end_date:
            queryset = queryset.filter(date__lte=end_date)
        
        return queryset.order_by('-date', '-time')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class AnalyticsView(LoginRequiredMixin, View):
    """Detailed analytics and insights"""
    
    def get(self, request):
        today = timezone.now().date()
        
        # Weekly breakdown
        week_start = today - timedelta(days=today.weekday())
        weekly_data = Transaction.objects.filter(
            date__gte=week_start,
            date__lte=today
        ).values('date').annotate(
            expense=Sum('amount', filter=Q(transaction_type='expense')),
            income=Sum('amount', filter=Q(transaction_type='income'))
        ).order_by('date')
        
        # Category breakdown (last 30 days)
        thirty_days_ago = today - timedelta(days=30)
        category_data = Transaction.objects.filter(
            date__gte=thirty_days_ago,
            transaction_type='expense'
        ).values('category__name').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')
        
        # Top spending days
        top_days = DailyLog.objects.filter(
            date__gte=thirty_days_ago
        ).order_by('-total_expense')[:10]
        
        # Average daily spending
        daily_logs = DailyLog.objects.filter(date__gte=thirty_days_ago)
        avg_daily = (daily_logs.aggregate(Sum('total_expense'))['total_expense__sum'] or Decimal('0')) / 30
        
        context = {
            'weekly_data': list(weekly_data),
            'category_data': list(category_data),
            'top_spending_days': top_days,
            'average_daily_expense': avg_daily,
        }
        
        return render(request, 'tracker/analytics.html', context)


class BudgetEditView(LoginRequiredMixin, View):
    """Update budget settings"""
    
    def get(self, request):
        budget = Budget.objects.first() or Budget.objects.create()
        form = BudgetForm(instance=budget)
        return render(request, 'tracker/budget_settings.html', {'form': form, 'budget': budget})
    
    def post(self, request):
        budget = Budget.objects.first() or Budget.objects.create()
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
        return render(request, 'tracker/budget_settings.html', {'form': form, 'budget': budget})


# API Views for M-Pesa integration
class MPesaWebhookView(View):
    """Receive M-Pesa transaction notifications"""
    
    def post(self, request):
        """
        Webhook endpoint for M-Pesa API callbacks
        Expected JSON format:
        {
            "Result": {
                "ResultCode": 0,
                "ResultDesc": "The service was requested successfully.",
                "OriginatorConversationID": "...",
                "ConversationID": "...",
                "TransactionID": "...",
                "ResultParameters": {
                    "ResultParameter": [
                        {"Key": "Amount", "Value": 1000},
                        {"Key": "TransactionDate", "Value": "20240101120000"},
                        {"Key": "TransactionType", "Value": "Pay Bill"},
                        ...
                    ]
                }
            }
        }
        """
        try:
            data = json.loads(request.body)
            result = data.get('Result', {})
            
            if result.get('ResultCode') == 0:
                params = result.get('ResultParameters', {}).get('ResultParameter', [])
                param_dict = {p['Key']: p['Value'] for p in params}
                
                # Extract transaction details
                amount = Decimal(str(param_dict.get('Amount', 0)))
                trans_date = param_dict.get('TransactionDate', '')
                trans_type = param_dict.get('TransactionType', 'Other')
                sender = param_dict.get('Sender', 'Unknown')
                transaction_id = result.get('TransactionID', '')
                
                # Parse date
                if trans_date:
                    date_obj = datetime.strptime(trans_date, '%Y%m%d%H%M%S').date()
                else:
                    date_obj = timezone.now().date()
                
                # Create transaction
                transaction, created = Transaction.objects.get_or_create(
                    mpesa_transaction_id=transaction_id,
                    defaults={
                        'amount': amount,
                        'date': date_obj,
                        'transaction_type': 'income',
                        'source': 'mpesa',
                        'description': f'M-Pesa: {sender}',
                    }
                )
                
                if created:
                    # Update daily log
                    daily_log, _ = DailyLog.objects.get_or_create(date=date_obj)
                    daily_log.total_income += amount
                    daily_log.save()
                
                return JsonResponse({'status': 'success'})
        
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
        
        return JsonResponse({'status': 'received'})
