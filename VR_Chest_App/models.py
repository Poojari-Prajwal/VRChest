from distutils.command.upload import upload
from email.policy import default
from pickle import TRUE
from django.db import models


CHOICES=(
    (5,"5"),
    (4.5,"4.5"),
    (4,"4"),
    (3.5,"3.5"),
    (3,"3"),
    (2.5,"2.5")
)

# Create your models here.
class Feedback(models.Model):
    id= models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    Email = models.CharField(max_length=50)
    Messege = models.TextField()

class Appointment(models.Model):
    id=models.AutoField(primary_key=True)
    Name = models.CharField(max_length=50)
    Mobileno=models.BigIntegerField()
    Email = models.CharField(max_length=50)
    Date = models.DateField()
    Doctor=models.CharField(max_length=30)
    RequestStatus=models.IntegerField(default=1) #1 for pending, 2 for accept and 3 for reject
    TimeSlots = models.CharField(max_length=50)

class Gallery_Image(models.Model):
    id=models.AutoField(primary_key=True)
    Image=models.ImageField(upload_to = "pics")

class Review(models.Model):
    id= models.AutoField(primary_key=True)
    Review_username = models.CharField(max_length = 50)
    Review_text = models.TextField(blank=True, null=True)
    rating= models.FloatField(choices=CHOICES, default=5)

class Article(models.Model):
    id=models.AutoField(primary_key=True)
    title=models.CharField(max_length=100, unique=True)
    content=models.TextField()
    slug=models.SlugField(max_length=100)
    link = models.CharField(max_length=200, null=True)
    



    