from django import forms
from apps.money.models import Money


class MoneyForm(forms.ModelForm):
    class Meta:
        model = Money
        fields = ['title', 'price', 'is_income']
