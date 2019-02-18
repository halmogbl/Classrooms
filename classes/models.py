from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
class Classroom(models.Model):
    name = models.CharField(max_length=120)
    subject = models.CharField(max_length=120)
    year = models.IntegerField()
    teacher = models.ForeignKey(User, default=1, on_delete=models.CASCADE)

    def get_absolute_url(self):
        return reverse('classroom-detail', kwargs={'classroom_id':self.id})

    def __str__(self):
        return self.name




gender_choices= (
    ('Male','Male'),
    ('Female','Female')
    )

class Student(models.Model):

    name = models.CharField(max_length=120)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=gender_choices)
    exam_grade = models.FloatField()
    classroom = models.ForeignKey(Classroom, on_delete=models.CASCADE)


    def __str__(self):
        return self.name













