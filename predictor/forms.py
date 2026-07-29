from django import forms

class HouseForm(forms.Form):
    sqft = forms.FloatField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 1500'}))
    bedrooms = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 3'}))
    bathrooms = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 2'}))
    age_of_house = forms.IntegerField(min_value=0, widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'e.g. 10'}))
    location = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. Suburb'}))

class CSVUploadForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))

class DatasetReplaceForm(forms.Form):
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}),
                           help_text='Upload CSV (columns: sqft,bedrooms,bathrooms,age_of_house,location,price)')