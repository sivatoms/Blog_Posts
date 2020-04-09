from django import forms

from .models import Transactions, GroupMembers


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
       