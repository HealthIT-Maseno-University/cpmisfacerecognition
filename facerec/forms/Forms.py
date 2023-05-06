from django import forms


class PhotoSearchForm(forms.Form):
    photo = forms.ImageField()
