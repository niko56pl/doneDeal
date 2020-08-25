from .models import Query
import django_filters

class QueryFilter(django_filters.FilterSet):
	class Meta:
		model = Query
		fields = ['MAKE', 'MODEL', 'YEAR', 'LITER', 'FUEL']