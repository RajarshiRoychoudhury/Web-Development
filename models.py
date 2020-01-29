from django.db import models

# Create your models here.
class Student(models.Model):
    first_name=models.CharField(max_length=50,default="first_name")
    last_name=models.CharField(max_length=50,default="last_name")
    username=models.CharField(max_length=12)
    course=models.CharField(max_length=20)
    department=models.CharField(max_length=20)
    email=models.EmailField(max_length=254)
    phone=models.CharField(max_length=20)
    library_card_issued=models.BooleanField(default=False)
    password=models.CharField(max_length=50)

    def __str__(self):
        return self.username

class Semester(models.Model):
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    year=models.IntegerField()
    semester=models.IntegerField()
    sub1_marks=models.IntegerField()
    sub2_marks=models.IntegerField()
    sub3_marks=models.IntegerField()
    sub4_marks=models.IntegerField()
    sub5_marks=models.IntegerField()
    sub1_marks=models.IntegerField(default=0)
    def __str__(self):
        return str(self.year)+" "+str(self.semester)    

    

