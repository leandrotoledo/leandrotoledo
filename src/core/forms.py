# -*- encoding: utf-8 -*-
from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(label='Nome:', max_length=100)
    sender = forms.EmailField(label='Endereço de e-mail:')
    site = forms.URLField(label='URL:')
    message = forms.CharField(label='Mensagem:', widget=forms.Textarea)
