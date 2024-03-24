from django.db import models
from django.contrib.auth import get_user_model
import uuid

from django.urls import reverse
User = get_user_model()


from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager


JOB_TYPE = (
    ('1', "Full OnBoard"),
    ('2', "Partly Onboard"),
    ('3', "Pending"),
)

class Vtype(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name
    

class Machine(models.Model):

    
    user = models.ForeignKey(User, related_name='MachineUser', on_delete=models.CASCADE) 
    title = models.CharField(max_length=300)
    description = RichTextField()
    tags = TaggableManager()
    location = models.CharField(max_length=300)
    job_type = models.CharField(choices=JOB_TYPE, max_length=1)
    vtype = models.ForeignKey(Vtype,related_name='VType', on_delete=models.CASCADE)
    capacity = models.CharField(max_length=30, blank=True)
    company_name = models.CharField(max_length=300)
    company_description = RichTextField(blank=True, null=True)
    url = models.URLField(max_length=200)
    last_date = models.DateField()
    is_published = models.BooleanField(default=False)
    is_unavailabled = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=True)
 
    


    def __str__(self):
        return self.title
       

 

class Client(models.Model):

    user = models.ForeignKey(User, related_name='ClientUser', on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)


    def __str__(self):
        return self.machine.title
        
class Vehicle(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)


    def __str__(self):
        return self.machine.title        


  

class BookmarkMachine(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)


    def __str__(self):
        return self.machine.title
