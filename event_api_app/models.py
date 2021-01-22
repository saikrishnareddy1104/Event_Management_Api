from django.db import models
import uuid 
# Create your models here.
class Events(models.Model):
    event_id = models.UUIDField( primary_key = True, default = uuid.uuid4,editable = False) 
    event_name = models.CharField(max_length=100)
    event_location = models.CharField(max_length=100)
    event_type = models.CharField(max_length=100)   
    organiser_email=models.EmailField(max_length=100)
    date=models.DateTimeField(auto_now_add=True)
    vacancy=models.IntegerField()
    def __str__(self):
        return self.event_name


class Participants(models.Model):   
    participant_id = models.UUIDField( primary_key = True, default = uuid.uuid4,editable = False)             
    username  = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    events_registerd =  models.ManyToManyField(Events)
    def __str__(self):
        return self.username   


