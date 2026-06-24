from django import forms
from .models import Transaction, Budget, Category


class TransactionForm(forms.ModelForm):
    """Form for adding/editing transactions"""
    
    class Meta:
        model = Transaction
        fields = ['amount', 'transaction_type', 'category', 'description', 'date', 'time', 'source']
        widgets = {
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Amount',
                'step': '0.01',
                'min': '0'
            }),
            'transaction_type': forms.Select(attrs={
                'class': 'form-control'
            }),
            'category': forms.Select(attrs={
                'class': 'form-control'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Description (optional)'
            }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date'
            }),
            'time': forms.TimeInput(attrs={
                'class': 'form-control',
                'type': 'time'
            }),
            'source': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.all()


class BudgetForm(forms.ModelForm):
    """Form for setting budget limits"""
    
    class Meta:
        model = Budget
        fields = ['daily_limit', 'monthly_limit', 'currency']
        widgets = {
            'daily_limit': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Daily Budget Limit',
                'step': '0.01',
                'min': '0'
            }),
            'monthly_limit': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Monthly Budget Limit',
                'step': '0.01',
                'min': '0'
            }),
            'currency': forms.Select(attrs={
                'class': 'form-control'
            }),
        }


class TransactionFilterForm(forms.Form):
    """Form for filtering transactions"""
    TRANSACTION_TYPE_CHOICES = [
        ('', '-- All --'),
        ('expense', 'Expenses'),
        ('income', 'Income'),
    ]
    
    transaction_type = forms.ChoiceField(
        choices=TRANSACTION_TYPE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label='-- All Categories --',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    start_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    end_date = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={
            'class': 'form-control',
            'type': 'date'
        })
    )
    min_amount = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Min Amount',
            'step': '0.01'
        })
    )
    max_amount = forms.DecimalField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Max Amount',
            'step': '0.01'
        })
    )
