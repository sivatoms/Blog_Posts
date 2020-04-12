from django.shortcuts import render, redirect

from django.contrib.auth.models import User
from .models import Transactions, Group, GroupMembers,Balance
from .forms import Bill_CreateForm, Bill_EditForm, Group_CreateForm
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
import re, math

def add_bills_home(request, id=None):
    user = User.objects.get(pk=id) 
    grpname = Group.objects.filter(groupmembers__members=user)
    gm = GroupMembers.objects.filter(group_name__group_name=grpname[0])    
    users_list = [i for i in gm]
    
    if request.method == 'POST':       
        form = Bill_CreateForm(users_list,request.POST)
        if form.is_valid():   
            print(form.cleaned_data['added_by'])
            added_by = User.objects.get(username=form.cleaned_data['added_by'])        
            form.cleaned_data['added_by'] = added_by.id
            print(added_by, added_by.id)
              
            form.save()
            t = Transactions.objects.last()
            #print(t, t.id)
            balances(t.id,form.cleaned_data['share_with'], form.cleaned_data['amount'], form.cleaned_data['bill_type'], user)
            form = Bill_CreateForm(users_list) 
              
            return render(request, 'bills/create_bill.html', {'form':form})
    else:        
        form = Bill_CreateForm(users_list)   
    return render(request, 'bills/create_bill.html', {'form':form})


def balances(id, user_list, amount, bill_type, paid_by):
    t = Transactions.objects.get(pk = id)
    bal = Balance()

    num_of_shares = len(user_list)

    due_each = float(amount)/num_of_shares

    if paid_by.username in user_list:
        bal.transaction = t
        bal.due_amount = due_each * (-(num_of_shares - 1))
        bal.paid_amount = amount
        bal.shared_with = user_list
        bal.user_name = paid_by
        bal.paid_by = paid_by.username
        bal.bill_type = bill_type
        bal.save()
    else:
        bal.transaction = t
        bal.due_amount = -amount
        bal.paid_amount = amount
        bal.shared_with = user_list
        bal.user_name = paid_by
        bal.paid_by = paid_by.username
        bal.bill_type = bill_type
        bal.save()
    
    for u in user_list:
        if paid_by.username != u:
            print("came here : ", u)
            bal = Balance()
            bal.transaction = t
            bal.due_amount = due_each
            bal.paid_amount = 0
            bal.shared_with = user_list
            bal.user_name = User.objects.get(username=u)
            bal.paid_by = paid_by.username  
            bal.bill_type = bill_type
            bal.save()

def balance_details(request, id=None):
    user = User.objects.get(pk=id)
    context = {}
    bal = Balance.objects.filter(user_name=user)
    total_due = 0
    for i in bal:
        shared = ', '.join(k for k in re.findall(r'[a-zA-Z]+', i.shared_with))
        #print('transactions is ',i.transaction)
        context[i.id] = {'Paid by': i.paid_by,
                         'Shared with': shared,
                         'Bill type': i.bill_type,
                         'Added on': i.purchase_date,
                         'Paid amount': round(i.paid_amount,2),
                         'Due amount' : round(i.due_amount,2) ,
                         'transaction':i.transaction                    
                          }
        total_due += i.due_amount
       
    context['total'] = {'Total Due': round(total_due,2)}


    return render(request, 'bills/balance_details.html', {'context':context})


def transaction_edit(request, id=None):
    trans = Transactions.objects.get(pk=id) 
    gmr = GroupMembers.objects.get(id=trans.added_by.id)
    user = User.objects.get(pk=gmr.members.id)
    grpname = Group.objects.filter(groupmembers__members=user)
    gm = GroupMembers.objects.filter(group_name__group_name=grpname[0])    
    users_list = [i for i in gm]
    if request.method == 'POST':       
        form = Bill_EditForm(users_list,request.POST, instance=trans)
        if form.is_valid():   
                added_by = User.objects.get(username=form.cleaned_data['added_by'])        
                form.cleaned_data['added_by'] = added_by.id               
                form.save()                    
                balances_update(request,trans.id,form.cleaned_data['share_with'], form.cleaned_data['amount'], form.cleaned_data['bill_type'], user)
                
                context = {'message':'Transaction has been updated!'}
                return render(request,  'bills/transaction_edit.html', context)
    else:
        form = Bill_EditForm(users_list,instance=trans)


    return render(request, 'bills/transaction_edit.html', {'form':form})




def balances_update(request,id, user_list, amount, bill_type, paid_by):
    t = Transactions.objects.get(pk = id)
    old_bal = Balance.objects.filter(transaction__id=id)
    old_bal.delete()

    bal = Balance()
    num_of_shares = len(user_list)

    due_each = float(amount)/num_of_shares

    if paid_by.username in user_list:
        bal.transaction = t
        bal.due_amount = due_each * (-(num_of_shares - 1))
        bal.paid_amount = amount
        bal.shared_with = user_list
        bal.user_name = paid_by
        bal.paid_by = paid_by.username
        bal.bill_type = bill_type
        bal.save()
    else:
        bal.transaction = t
        bal.due_amount = -amount
        bal.paid_amount = amount
        bal.shared_with = user_list
        bal.user_name = paid_by
        bal.paid_by = paid_by.username
        bal.bill_type = bill_type
        bal.save()

    for u in user_list:
        if paid_by.username != u:
            bal = Balance()
            bal.transaction = t
            bal.due_amount = due_each
            bal.paid_amount = 0
            bal.shared_with = user_list
            bal.user_name = User.objects.get(username=u)
            bal.paid_by = paid_by.username  
            bal.bill_type = bill_type
            bal.save()
    
    


def delete_transaction(request, id):
    t = Transactions.objects.get(pk=id)
    if request.POST:
        if 'delete' in request.POST:
            t.delete()
            context = {'message':'Transaction '+t.bill_type+' has been deleted!'}
            return render(request, 'bills/transaction_delete.html', context)
    return render(request, 'bills/transaction_delete.html')


def group_create(request):
    if request.POST:
        new_group_form = Group_CreateForm(request.POST)
        if new_group_form.is_valid():
            new_group_form.save()
            return redirect('post_list')
    else:
        new_group_form = Group_CreateForm(request.POST)
    return render(request, 'bills/create_group.html', {'form':new_group_form})