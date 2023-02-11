from django.db import models

# Create your models here.
class Person(models.Model):
    name = models.CharField(max_length=100)
    image= models.CharField(max_length=250)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Model person is {self.name}'