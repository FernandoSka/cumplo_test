from django import forms

class DateForm(forms.Form):
    gte = forms.DateField(widget=forms.DateInput(attrs={
            'type': 'date',
        }))
    lte = forms.DateField(widget=forms.DateInput(attrs={
            'type': 'date',
        }))

    def clean_lte(self):
    	if self.cleaned_data["gte"] > self.cleaned_data["lte"]:
    		raise forms.ValidationError(u'The initial date must be lower than final date')
    	return self.cleaned_data["lte"]