from django import forms

from .models import Transactions, GroupMembers,Group


class Bill_CreateForm(forms.ModelForm):

    def __init__(self, user_list, *args, **kwargs):          
        super(Bill_CreateForm, self).__init__(*args, **kwargs)
        self.fields['share_with'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=tuple([(name, name.members) for name in user_list]))
        #self.fields['added_by'] = forms.ChoiceField(choices=tuple([(name, name.members) for name in user_list]))
       
    class Meta:
        model = Transactions
        fields = (
            'bill_type',
            'amount',
            'added_by',
            'added_to',
            'share_with',
        )

class Bill_EditForm(forms.ModelForm):

    def __init__(self, user_list, *args, **kwargs):          
        super(Bill_EditForm, self).__init__(*args, **kwargs)
        self.fields['share_with'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,choices=tuple([(name, name.members) for name in user_list]))
        #self.fields['added_by'] = forms.ChoiceField(choices=tuple([(name, name.members) for name in user_list]))
       
    class Meta:
        model = Transactions
        fields = (
            'bill_type',
            'amount',
            'added_by',
            'added_to',
            'share_with',
        )

class Group_CreateForm(forms.ModelForm):
    class Meta:
        model = Group
        fields=[
            'group_name',
        ]
    