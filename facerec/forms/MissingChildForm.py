from django import forms

from facerec.models import MissingChild


class MissingChildForm(forms.ModelForm):
    class Meta:
        model = MissingChild
        fields = ['first_name', 'last_name',
                  'current_age', 'gender', 'photo', 'date_missing',
                  'date_of_birth'
                  ]
