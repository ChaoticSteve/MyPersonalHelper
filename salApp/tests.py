from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse

from .models import LessonModel


class LessonModelTests(TestCase):
    def test_online_rates(self):
        lesson = LessonModel.objects.create(date='2026-01-01', lesson_format='online', lesson_type='individual')
        self.assertEqual(lesson.amount, Decimal('2500'))

        lesson = LessonModel.objects.create(
            date='2026-01-01', lesson_format='online', lesson_type='group', students_count=7
        )
        self.assertEqual(lesson.amount, Decimal('5000'))

    def test_offline_group_tiers(self):
        l1 = LessonModel.objects.create(
            date='2026-01-01', lesson_format='offline', lesson_type='group', students_count=4
        )
        self.assertEqual(l1.amount, Decimal('4000'))

        l2 = LessonModel.objects.create(
            date='2026-01-02', lesson_format='offline', lesson_type='group', students_count=10
        )
        self.assertEqual(l2.amount, Decimal('6000'))

        l3 = LessonModel.objects.create(
            date='2026-01-03', lesson_format='offline', lesson_type='group', students_count=11
        )
        self.assertEqual(l3.amount, Decimal('6600'))

    def test_group_requires_students(self):
        lesson = LessonModel(date='2026-01-01', lesson_format='offline', lesson_type='group')
        with self.assertRaises(ValidationError):
            lesson.full_clean()


class ViewsTests(TestCase):
    def test_pages_render(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('report'))
        self.assertEqual(response.status_code, 200)
