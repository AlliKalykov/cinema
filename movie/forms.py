from django import forms

from .models import Movie

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ('name', 'long_time', 'start_date', 'end_date', 'company', 'is_active')
 

# class MovieForm2(forms.Form):
#     name = forms.CharField(max_length=100, label='Название')
#     long_time = forms.IntegerField(label='Длительность')
#     start_date = forms.DateField(label='Дата выхода')
#     end_date = forms.DateField(label='Дата окончания')
#     company = forms.CharField(max_length=100, label='Прокатчик')
#     is_active = forms.BooleanField(label='Активен')