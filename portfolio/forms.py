from django import forms 
from pats.models import ContactInfo, ContactMich


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.CharField()
    message = forms.CharField()

class ContactModelForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea())
    class Meta:
        model = ContactInfo
        fields = [
            'name',
            'email',
            'message',
        ]

class ContactMichForm(forms.Form):
    name = forms.CharField()
    email = forms.CharField()
    message = forms.CharField()

class ContactMichModelForm(forms.ModelForm):
    message = forms.CharField(widget=forms.Textarea())
    class Meta:
        model = ContactMich
        fields = [
            'name',
            'email',
            'message',
        ]
#     validate form here

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['name'].widget.attrs.update({'class':'form-control'})
    #     self.fields['email'].widget.attrs.update({'class':'form-control'})
    #     self.fields['message'].widget.attrs.update({'class':'form-control'})





        