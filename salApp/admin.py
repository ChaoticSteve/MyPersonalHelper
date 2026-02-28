from django.contrib import admin

from .models import LessonModel


@admin.register(LessonModel)
class LessonModelAdmin(admin.ModelAdmin):
    list_display = ('date', 'lesson_format', 'lesson_type', 'students_count', 'amount')
    list_filter = ('lesson_format', 'lesson_type', 'date')
    search_fields = ('date',)
