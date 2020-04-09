from django.contrib import admin

from .models import Group, GroupMembers, Transactions, Balance
# Register your models here.

admin.site.register(Group)
admin.site.register(GroupMembers)
admin.site.register(Transactions)
admin.site.register(Balance)
