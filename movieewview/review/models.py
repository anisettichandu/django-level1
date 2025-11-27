from django.db import models

class Movie_details(models.Model):
    movie_name=models.CharField(max_length=100,unique=True)
    release_date=models.DateField(max_length=100)
    budget=models.CharField(max_length=100)
    rating=models.FloatField(max_length=100)
    
class Stu_details(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField(max_length=100)
    password=models.CharField(max_length=100)
    
