from django.db import models
from django.utils import timezone
from django.db.models import Sum


class Balance(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, unique=True)
    balance = models.IntegerField()

    def __int__(self):
        return self.balance



class Money(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=221)
    price = models.IntegerField()
    is_income = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    @classmethod
    def calculate_left_money(cls, user):
        now = timezone.now()
        start_of_month = now.replace(day=1)

        current_month_money = cls.objects.filter(
            user=user,
            created_date__gte=start_of_month,
            created_date__lt=now
        )

        left_money = current_month_money.aggregate(Sum('price'))['price__sum'] or 0

        return left_money

    @classmethod
    def calculate_previous_month_left_money(cls, user):
        now = timezone.now()
        first_day_of_current_month = now.replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timezone.timedelta(days=1)
        first_day_of_previous_month = last_day_of_previous_month.replace(day=1)

        previous_month_money = cls.objects.filter(
            user=user,
            created_date__gte=first_day_of_previous_month,
            created_date__lte=last_day_of_previous_month
        )

        previous_month_left_money = previous_month_money.aggregate(Sum('price'))['price__sum'] or 0

        return previous_month_left_money