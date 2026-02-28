from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import models


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
    lesson_type = models.CharField(max_length=20, choices=LESSON_TYPES, verbose_name='Тип урока')
    lesson_format = models.CharField(max_length=10, choices=FORMATS, verbose_name='Формат урока')
    students_count = models.PositiveIntegerField(
        verbose_name='Количество детей',
        null=True,
        blank=True,
        help_text='Обязательно для групповых уроков',
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма', default=Decimal('0.00'))
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return (
            f"{self.get_lesson_type_display()} "
            f"({self.get_lesson_format_display()}) — {self.date.strftime('%d.%m.%Y')}"
        )

    def clean(self):
        super().clean()

        if self.lesson_type == 'group' and not self.students_count:
            raise ValidationError({'students_count': 'Для группового урока укажите количество учеников.'})

        if self.lesson_type != 'group' and self.students_count:
            raise ValidationError({'students_count': 'Количество учеников заполняется только для групповых уроков.'})

    def calculate_amount(self):
        # Онлайн тарифы
        if self.lesson_format == 'online':
            if self.lesson_type == 'individual':
                return Decimal('2500')
            if self.lesson_type == 'group':
                return Decimal('5000')
            if self.lesson_type == 'masterclass':
                return Decimal('2000')
            if self.lesson_type == 'makeup':
                return Decimal('1000')

        # Оффлайн тарифы
        if self.lesson_format == 'offline':
            if self.lesson_type == 'individual':
                return Decimal('2500')
            if self.lesson_type == 'masterclass':
                return Decimal('2000')
            if self.lesson_type == 'makeup':
                return Decimal('1000')
            if self.lesson_type == 'group':
                if not self.students_count:
                    raise ValidationError('Для оффлайн группового урока требуется количество учеников.')
                if self.students_count <= 4:
                    return Decimal('4000')
                if self.students_count <= 10:
                    return Decimal('6000')
                return Decimal('600') * self.students_count

        raise ValidationError('Не удалось определить тариф для выбранных параметров урока.')

    def save(self, *args, **kwargs):
        self.full_clean()
        self.amount = self.calculate_amount()
        super().save(*args, **kwargs)
