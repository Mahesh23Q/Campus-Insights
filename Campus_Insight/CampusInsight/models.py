from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone
import datetime

# Create your models here.

class User(AbstractUser):
	role = [
		('S',"Student"),
		('T',"Faculty"),
		('A',"admin")
	]
	user_role = models.CharField(default='S',choices=role,max_length=6)


from datetime import timedelta
from django.db import models
from django.utils import timezone

class Exam(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    docx_file = models.FileField(upload_to='exams/', null=True, blank=True)  # Optional field
    date = models.DateField(default=timezone.now)  # Date of the exam
    start_time = models.TimeField()  # Start time of the exam
    duration = models.DurationField(default=timedelta())  # Default duration of 0:00:00

    def __str__(self):
        return self.title

    @property
    def end_time(self):
        """Calculate the end time of the exam based on the start time and duration."""
        return (timezone.make_aware(datetime.combine(self.date, self.start_time)) + self.duration).time()

class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option1 = models.CharField(max_length=255)
    option2 = models.CharField(max_length=255)
    option3 = models.CharField(max_length=255)
    option4 = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=255)  # This will store the correct answer

    def __str__(self):
        return self.question_text
