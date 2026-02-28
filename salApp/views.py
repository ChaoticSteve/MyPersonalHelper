from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.shortcuts import redirect, render
from django.utils import timezone

from .forms import LessonForm, MonthFilterForm
from .models import LessonModel


def _monthly_context(year: int, month: int):
    lessons = LessonModel.objects.filter(date__year=year, date__month=month)
    total = lessons.aggregate(total=Sum('amount'))['total'] or 0

    daily_rows = (
        lessons.annotate(day=TruncDate('date'))
        .values('day')
        .annotate(day_total=Sum('amount'))
        .order_by('day')
    )

    return {
        'year': year,
        'month': month,
        'lessons': lessons.order_by('-date', '-created_at'),
        'daily_rows': daily_rows,
        'month_total': total,
    }


def index(request):
    today = timezone.localdate()

    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = LessonForm(initial={'date': today})

    context = {
        'form': form,
        **_monthly_context(today.year, today.month),
    }
    return render(request, 'salApp/index.html', context)


def report(request):
    today = timezone.localdate()

    initial = {'year': today.year, 'month': today.month}
    form = MonthFilterForm(request.GET or None, initial=initial)

    if form.is_valid():
        year = form.cleaned_data['year']
        month = form.cleaned_data['month']
    else:
        year = today.year
        month = today.month

    context = {
        'filter_form': form,
        **_monthly_context(year, month),
    }
    return render(request, 'salApp/report.html', context)
