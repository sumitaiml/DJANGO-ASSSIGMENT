from django.db import models
from django.contrib.auth.models import User


class ExamForm(models.Model):
    YEAR_CHOICES = [
        ('1', 'First Year'),
        ('2', 'Second Year'),
        ('3', 'Third Year'),
        ('4', 'Fourth Year'),
    ]

    # Link each form submission to the logged-in student
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='exam_forms')

    full_name    = models.CharField(max_length=150)
    course       = models.CharField(max_length=100)
    year         = models.CharField(max_length=1, choices=YEAR_CHOICES)
    address      = models.TextField()
    phone_number = models.CharField(max_length=15)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} — {self.course} (Year {self.year})"
