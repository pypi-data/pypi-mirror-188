from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(
        label='', max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'})
    )
    phone = forms.CharField(
        label='', max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Phone', 'class': 'form-control'})
    )
    message = forms.CharField(
        label='',
        required=False,
        widget=forms.Textarea(attrs={'placeholder': 'Message',
                                     'class': 'form-control',
                                     'rows': '4'}))


class MailinglistForm(forms.Form):
    name = forms.CharField(
        label='', max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'Name', 'class': 'form-control'})
    )
    email = forms.CharField(
        label='', max_length=20,
        widget=forms.TextInput(attrs={'placeholder': 'E-Mail', 'class': 'form-control'})
    )