from django.urls import path
from apps.money.views import index

urlpatterns = [
    path('', index, name="index"),
]