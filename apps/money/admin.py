from django.contrib import admin
from apps.money.models import Money, Balance


@admin.register(Money)
class MoneyAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'title', 'price')


@admin.register(Balance)
class BalanceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'balance')
