from django.http import HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from apps.money.models import Money, Balance
from apps.money.forms import MoneyForm
import datetime
import calendar
from django.utils import timezone


def index(request):
    # GET
    user_id = request.user.id

    # Filter all Money entries for the current month only
    now = timezone.now()
    start_of_month = now.replace(day=1)
    all_money = Money.objects.filter(
        user_id=user_id,
        created_date__gte=start_of_month,
        created_date__lt=now
    ).order_by('-id')

    left_money = (Balance.objects.filter(user_id=user_id).values_list('balance', flat=True).first()) - (
        Money.calculate_left_money(user_id))
    balance = Balance.objects.filter(user_id=user_id).values_list('balance', flat=True).first()
    all_spendings = Money.calculate_left_money(user_id)
    today = datetime.datetime.now()
    current_month_number = today.month
    current_month_name = calendar.month_name[current_month_number]
    previous_month_number = current_month_number - 1 if current_month_number > 1 else 12
    previous_month_name = calendar.month_name[previous_month_number]
    two_months = ((Money.calculate_previous_month_left_money(user_id)) - all_spendings) * (-1)

    # POST
    form = MoneyForm()
    if request.method == "POST":
        form = MoneyForm(request.POST)
        if form.is_valid():
            money_instance = form.save(commit=False)
            money_instance.user_id = user_id
            money_instance.save()
            return redirect("index")

    # DELETE
    if request.method == "POST" and 'delete_id' in request.POST:
        money_id = request.POST.get('delete_id')
        if money_id:
            money_instance = get_object_or_404(Money, id=money_id, user_id=user_id)
            money_instance.delete()
            return redirect("index")

    context = {
        "all_money": all_money,
        "left_money": left_money,
        "balance": balance,
        "all_spendings": all_spendings,
        "current_month": current_month_name,
        "previous_month": previous_month_name,
        "two_months": two_months,
        "form": form,
    }
    return render(request, 'index.html', context)
