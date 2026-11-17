from django import forms
from .models import Student, Module

class StudentEditForm(forms.ModelForm):

    class Meta:
        model = Student
        fields = '__all__'
        widgets = {
            'enrolmentDate': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M', attrs={'type': 'datetime-local'}
            ),
        }

class StudentFilterForm(forms.Form):
    firstName = forms.CharField(label='First name contains', required=False)
    lastName = forms.CharField(label='Last name contains', required=False)
    min_age = forms.IntegerField(label='Age greater than', required=False, min_value=0)
    max_age = forms.IntegerField(label='Age less than', required=False, min_value=0)
    module = forms.ModelChoiceField(queryset=Module.objects.all(), required=False)
    module_name = forms.CharField(label='Module name contains', required=False)
