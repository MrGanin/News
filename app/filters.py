from django_filters import FilterSet, DateFilter
from .models import Post
from django.forms import DateInput
class PostFilter(FilterSet):
    date = DateFilter(
        field_name = 'date',
        widget = DateInput(attrs={'type':'date'}),
        label = 'Date',
        lookup_expr = 'date__lt',
    )
    class Meta:
       model = Post
       fields = {
           'title':['icontains'],
           'author':['exact'],

       }