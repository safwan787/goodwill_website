

from django import forms
from store_admin.models import Inquiry

class InquiryForm(forms.ModelForm):

    class Meta:
        model = Inquiry
        fields = ['name', 'email', 'phone', 'message']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mobile Number'}),
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }

