from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = [
            'claim_type',
            'travel_type',
            'city',
            'date',
            'expense',
            'currency',
            'conversion_rate',
            # 'unit_value',
            'amount',
            'final_amount',
            'project',
            'document',
            'bill',
            'remarks'
        ]

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    # ✅ OPTIONAL: auto calculate final_amount (safe add, no removal)
    def clean(self):
        cleaned_data = super().clean()
        amount = cleaned_data.get("amount")
        rate = cleaned_data.get("conversion_rate")

        if amount and rate:
            cleaned_data["final_amount"] = amount * rate

        return cleaned_data