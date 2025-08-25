from django.db import models


# Create your models here.

class LessonRateModel(models.Model):
    LESSON_TYPES = [
        ('group', 'Групповой'),
        ('individual', 'Индивидуальный'),
        ('masterclass', 'Мастер-класс'),
        ('makeup', 'Отработка'),
    ]
    FORMATS = [
        ('online', 'Онлайн'),
        ('offline', 'Оффлайн'),
    ]
    lesson_format = models.CharField(
        max_length=10,
        choices=FORMATS,
        verbose_name='Формат урока'
    )
    lesson_type = models.CharField(
        max_length=20,
        choices=LESSON_TYPES,
        verbose_name='Тип урока'
    )


class LessonModel(models.Model):
    LESSON_TYPES = [
        ('group', 'Групповой'),
        ('individual', 'Индивидуальный'),
        ('masterclass', 'Мастер-класс'),
        ('makeup', 'Отработка'),
    ]
    FORMATS = [
        ('online', 'Онлайн'),
        ('offline', 'Оффлайн'),
    ]
    date = models.DateField(verbose_name='Дата урока')
    lesson_type = models.CharField(
        max_length=20,
        choices=LESSON_TYPES,
        verbose_name='Тип урока'
    )
    lesson_format = models.CharField(
        max_length=10,
        choices=FORMATS,
        verbose_name='Формат урока'
    )
    students_count = models.PositiveIntegerField(
        verbose_name='Количество детей',
        null=True,
        blank=True
    )
    amount = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        verbose_name='Сумма',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = 'Урок',
        verbose_name_plural = 'Уроки',
        ordering = ['-date']

    def __str__(self):
        return f"{self.get_lesson_type_display()} ({self.get_format_display()}) — {self.date.strftime('%d.%m.%Y')}"

    def calculate_amount(self):

        rate = LessonRateModel.objects.filter(
            format = self.lesson_format,
            lesson_type = self.lesson_type,
        ).filter(
            models.Q(min_students__lte=self.students_count) | models.Q(min_students__isnull=True),
            models.Q(max_students__gte=self.students_count) | models.Q(max_students__isnull=True)
        ).first()

        if rate:
            if rate.per_student and self.students_count:
                return self.students_count * rate.rate
            return rate.rate
        return self.amount
    def save(self, *args, **kwargs):
        calculated = self.calculate_amount()
        if calculated:
            self.amount = calculated
        super().save(*args, **kwargs)


