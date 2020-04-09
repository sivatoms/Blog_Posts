from django.db import models

from django.contrib.auth.models import User

class Group(models.Model):
    group_name = models.CharField('Group name', max_length=50)

    def __str__(self):
        return self.group_name


class GroupMembers(models.Model):
    group_name = models.ManyToManyField(Group)
    members = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.members.username

class Transactions(models.Model):
    bill_type = models.CharField('Bill type',max_length=200)
    added_by = models.ForeignKey(GroupMembers, on_delete=models.CASCADE)
    added_to = models.ForeignKey(Group, on_delete=models.CASCADE)
    purchase_date = models.DateField(auto_now=True)
    share_with = models.CharField('Share among',max_length=250)
    amount = models.FloatField(default=0)

    def __str__(self):
        return self.bill_type


class Balance(models.Model):
    transaction = models.ForeignKey(Transactions, on_delete=models.CASCADE)
    bill_type = models.CharField('Bill type', max_length=50, null=False, blank=False, default='Grocery type')
    user_name = models.ForeignKey(User,on_delete=models.CASCADE)
    paid_by = models.CharField(max_length=150, null=True, blank=True)
    paid_amount = models.FloatField('You Spent', default=0,null=True, blank=True)
    due_amount = models.FloatField('You Owe', default=0,null=True, blank=True)
    shared_with = models.CharField("Shared With", max_length=250)
    purchase_date = models.DateField(auto_now=True)

    def __unicode__(self):
        return self.user_name