from django.urls import path, include
from .views import add_bills_home, balance_details, transaction_edit, delete_transaction,group_create

urlpatterns =[
    path('<int:id>',add_bills_home, name='add_bills_home'),
    path('balance_details/<int:id>',balance_details, name='balance_details'),
    path('balance_details/transaction_edit/<int:id>',transaction_edit, name='transaction_edit'),
    path('transaction_delete/<int:id>',delete_transaction, name='transaction_delete'),
    path('group_create',group_create, name='group_create'),
]
