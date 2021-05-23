from django import forms

class PaymentForm(forms.Form):
    url = forms.URLField(required=True,
                         widget=forms.TextInput
                         (attrs={'placeholder': ('URL of tweet containing thenewboston address...')}))
    amount = forms.IntegerField()
