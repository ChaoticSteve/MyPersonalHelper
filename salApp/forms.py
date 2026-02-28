from django import forms

from .models import LessonModel


class LessonForm(forms.ModelForm):
    class Meta:
        model = LessonModel
        fields = ['date', 'lesson_format', 'lesson_type', 'students_count']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }


class MonthFilterForm(forms.Form):
    year = forms.IntegerField(min_value=2020, max_value=2100, label='Год')
    month = forms.IntegerField(min_value=1, max_value=12, label='Месяц')
