from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('add/', views.TransactionCreateView.as_view(), name='add_transaction'),
    path('history/', views.TransactionListView.as_view(), name='transaction_list'),
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    path('budget/', views.BudgetEditView.as_view(), name='budget_edit'),
]
