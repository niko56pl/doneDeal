from django import forms  
from .models import Query, Average, YEARS, MAKES, MODELS, LITERS, FUELS, MILEAGES, DATES
import django_filters

class QueryForm(forms.ModelForm):  
	error_css_class = 'error'
	
	YEAR = forms.ChoiceField(choices=YEARS)
	MAKE = forms.ChoiceField(choices=MAKES, required=True )
	MODEL = forms.ChoiceField(choices=MODELS, required=True )
	LITER = forms.ChoiceField(choices=LITERS )
	FUEL = forms.ChoiceField(choices=FUELS )
	#MILEAGE = forms.ChoiceField(choices=MILEAGES )
	#ENTERED = forms.ChoiceField(choices=DATES )
	
	class Meta:
		model = Query
		fields = ['MAKE', 'MODEL', 'YEAR', 'LITER', 'FUEL']		#'__all__' 

	#def __init__(self, *args, **kwargs):
		#super().__init__(*args, **kwargs)
		#self.fields['MODEL'].queryset = #
		
#class QueryFilter(django_filters.FilterSet):

		"""
		widgets = {
			'year': forms.TextInput(attrs={'placeholder': 'Year of registration'}),
			'make': forms.TextInput(attrs={'placeholder': 'Make of the car'}),
			'model': forms.TextInput(attrs={'placeholder': 'Model of the car'}),
			'liter': forms.TextInput(attrs={'placeholder': 'Engine Capacity in Litres'}),
			'fuel': forms.TextInput(attrs={'placeholder': 'Fuel type e.g. Petrol'}),
			'mileage': forms.TextInput(attrs={'placeholder': 'Mileage of the car'}),
			#'entered': forms.TextInput(attrs={'placeholder': 'Year/Month'})
		}
		"""