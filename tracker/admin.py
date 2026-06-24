from django.contrib import admin
from .models import Transaction, Budget, Category, DailyLog


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('daily_limit', 'monthly_limit', 'currency', 'updated_at')
    fieldsets = (
        ('Budget Limits', {
            'fields': ('daily_limit', 'monthly_limit')
        }),
        ('Currency', {
            'fields': ('currency',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('date', 'amount', 'transaction_type', 'category', 'description', 'source')
    list_filter = ('transaction_type', 'category', 'source', 'date')
    search_fields = ('description', 'mpesa_transaction_id')
    readonly_fields = ('created_at', 'updated_at', 'mpesa_transaction_id')
    
    fieldsets = (
        ('Transaction Details', {
            'fields': ('amount', 'transaction_type', 'category', 'description')
        }),
        ('Date & Time', {
            'fields': ('date', 'time')
        }),
        ('Source', {
            'fields': ('source', 'mpesa_transaction_id')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('category')


@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ('date', 'total_expense', 'total_income', 'net', 'transaction_count', 'is_logged')
    list_filter = ('is_logged', 'date')
    search_fields = ('date',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Daily Summary', {
            'fields': ('date', 'total_expense', 'total_income', 'transaction_count')
        }),
        ('Status', {
            'fields': ('is_logged',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    @admin.display(description='Net (Income - Expense)')
    def net(self, obj):
        return obj.total_income - obj.total_expense
