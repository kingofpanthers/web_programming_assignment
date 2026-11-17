from django import forms

class HashForm(forms.Form):
    text = forms.CharField(label='Enter text here:', strip=False, widget=forms.Textarea, max_length=10000)
