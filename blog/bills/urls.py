from django.urls import path, include
from .views import add_bills_home, balance_details

urlpatterns =[
    path('<int:id>',add_bills_home, name='add_bills_home'),
    path('balance_details/<int:id>',balance_details, name='balance_details'),
]